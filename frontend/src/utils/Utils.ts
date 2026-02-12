import { modalController } from "@ionic/vue";

/** * Interface for environment-agnostic configuration.
 * Docker deployments benefit from flat, environment-variable-driven structures.
 */
interface AppConfig {
  baseUrl: string;
  basePath: string;
  apiVersion: string;
  port?: string;
  appTitle: string;
  cacheExpiryH: number;
}

/**
 * Docker/Runtime Configuration Resolver
 */
const getRuntimeConfig = (): AppConfig => {
  const env = (window as any)._env_ || import.meta.env || {};

  return {
    baseUrl: env.VITE_API_BASE_URL || "http://localhost",
    basePath: env.VITE_API_BASE_PATH || "/api",
    apiVersion: env.VITE_API_VERSION || "/v1",
    port: env.VITE_API_PORT || "",
    appTitle: env.VITE_APP_TITLE || "SkillPlate",
    cacheExpiryH: Number(env.VITE_CACHE_EXPIRY_H) || 24,
  };
};

const CONFIG = getRuntimeConfig();

/** Pre-computed API URL */
const API_URL = (() => {
  const portSuffix = CONFIG.port ? `:${CONFIG.port}` : "";
  return `${CONFIG.baseUrl}${portSuffix}${CONFIG.basePath}${CONFIG.apiVersion}`;
})();

/** Pre-computed expiry threshold in milliseconds */
const CACHE_EXPIRY_MS = CONFIG.cacheExpiryH * 60 * 60 * 1000;

/**
 * Global Utility Service
 */
const Utils = {
  /** Returns the active configuration object */
  getConfig() {
    return CONFIG;
  },

  /** Returns the application title */
  getAppTitle(): string {
    return CONFIG.appTitle;
  },

  /** Returns the pre-computed API Base URL */
  getApiBaseUrl(): string {
    return API_URL;
  },

  /** Determines if a specific timestamp has exceeded the cache lifetime */
  isCacheExpired(timestamp: number): boolean {
    return Date.now() - timestamp > CACHE_EXPIRY_MS;
  },

  /** * Converts an ISO date string to epoch milliseconds.
   * Native Date.parse() handles ISO 8601 (including 'Z' or offsets) efficiently.
   */
  convertToMillis(dateString: string): number {
    const ms = Date.parse(dateString);
    return isNaN(ms) ? 0 : ms;
  },

  /**
   * High-performance array filter for search queries.
   */
  baseSearchFilter<T extends object>(query: string, toFilter: T[]): T[] {
    if (!query || !toFilter?.length) return toFilter;

    const lowerQuery = query.trim().toLowerCase();
    if (!lowerQuery) return toFilter;

    return toFilter.filter((item) => {
      for (const key in item) {
        if (Object.prototype.hasOwnProperty.call(item, key)) {
          const value = item[key as keyof T];
          if (
            typeof value === "string" &&
            value.toLowerCase().includes(lowerQuery)
          ) {
            return true;
          }
        }
      }
      return false;
    });
  },

  /** * Converts a date string to a localized, human-readable format using native Intl.
   * Replaces Luxon's DATETIME_MED_WITH_WEEKDAY.
   */
  convertDateString(dateString: string): string {
    if (!/^\d{4}-\d{2}-\d{2}/.test(dateString)) {
      return dateString;
    }

    const date = new Date(dateString);
    
    // Check for "Invalid Date"
    if (isNaN(date.getTime())) {
      return dateString;
    }

    // Equivalent to Luxon's DATETIME_MED_WITH_WEEKDAY
    // e.g., "Monday, Jan 24, 2026, 12:43 PM"
    return new Intl.DateTimeFormat(undefined, {
      weekday: 'short',
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: 'numeric',
      minute: 'numeric'
    }).format(date);
  },

  /** Capitalizes only the first letter of a string */
  capitalizeFirstLetter(str: string): string {
    return str ? str.charAt(0).toUpperCase() + str.slice(1) : "";
  },

  /** Standard debounce to limit function execution frequency */
  debounce<F extends (...args: any[]) => any>(fn: F, delay: number) {
    let timeout: number | undefined;
    return (...args: Parameters<F>) => {
      window.clearTimeout(timeout);
      timeout = window.setTimeout(() => fn(...args), delay);
    };
  },

  /** Closes the active top-most Ionic modal */
  async closeOpenModal(): Promise<void> {
    const topModal = await modalController.getTop();
    if (topModal) {
      await modalController.dismiss();
    }
  },

  /** Recursively dismisses all currently open Ionic modals */
  async closeAllOpenModals(): Promise<void> {
    let topModal = await modalController.getTop();
    while (topModal) {
      await modalController.dismiss();
      topModal = await modalController.getTop();
    }
  },
};

export default Utils;