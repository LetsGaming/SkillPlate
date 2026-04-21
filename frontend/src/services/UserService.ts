import { BaseService } from '@/services/base/BaseService';
import ApiUtils from '@/utils/ApiUtils';
import TokenUtils from '@/utils/TokenUtils';
import storageService from '@/services/general/StorageService';
import router from '@/router';
import Utils from '@/utils/Utils';

const BASE_ENDPOINT = '/auth';
const RESOURCE_KEY = 'auth.title';

export default class UserService extends BaseService {
  // ---------------------------------------------------------------------------
  // Token helpers
  // ---------------------------------------------------------------------------

  private static decodeToken(token: string): AuthToken | null {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return { id: payload.sub ?? payload.id, username: payload.username, role: payload.role };
    } catch {
      return null;
    }
  }

  private static async getDecodedToken(): Promise<AuthToken | null> {
    const token = await TokenUtils.getToken();
    return token ? this.decodeToken(token) : null;
  }

  // ---------------------------------------------------------------------------
  // Auth actions
  // ---------------------------------------------------------------------------

  static async login(data: LoginData): Promise<void> {
    const response = await this.handleRequest<LoginResponseData>(
      ApiUtils.post(BASE_ENDPOINT + '/login', data),
      RESOURCE_KEY,
      'auth.login_failed',
    );
    await TokenUtils.setToken(response.access_token);
  }

  static async logout(): Promise<void> {
    try {
      await ApiUtils.post(BASE_ENDPOINT + '/logout', null);
    } catch (error) {
      console.error('Server logout error:', error);
    } finally {
      await TokenUtils.clearToken();
      await storageService.clear();
      router.replace({ name: 'login' });
    }
  }

  /**
   * Uses the HttpOnly refresh-token cookie to get a new access token.
   * Endpoint: POST /api/refresh
   */
  static async refreshToken(retryCount = 3): Promise<string> {
    const url = `${Utils.getApiBaseUrl()}${BASE_ENDPOINT}/refresh`;

    for (let attempt = 1; attempt <= retryCount; attempt++) {
      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
        });

        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const res = await response.json();
        const accessToken: string | undefined = res?.data?.access_token;
        if (!accessToken) throw new Error('Missing access_token in refresh response');

        await TokenUtils.setToken(accessToken);
        return accessToken;
      } catch (error) {
        if (attempt === retryCount) throw error;
        await new Promise((resolve) => setTimeout(resolve, 1000 * attempt));
      }
    }

    throw new Error('Token refresh failed after all retries');
  }

  // ---------------------------------------------------------------------------
  // Identity & role getters
  // ---------------------------------------------------------------------------

  static async isAuthenticated(): Promise<boolean> {
    const token = await TokenUtils.getToken();
    if (token) return true;

    // No access token — try refreshing via HttpOnly cookie
    try {
      await this.refreshToken(1);
      return !!(await TokenUtils.getToken());
    } catch {
      return false;
    }
  }

  static async getUsername(): Promise<string> {
    return (await this.getDecodedToken())?.username ?? '';
  }

  static async getUserRole(): Promise<UserRole | null> {
    return (await this.getDecodedToken())?.role ?? null;
  }

  static async getUserId(): Promise<number> {
    return (await this.getDecodedToken())?.id ?? -1;
  }

  static async isAdmin(): Promise<boolean> {
    return (await this.getUserRole()) === 'admin';
  }
}
