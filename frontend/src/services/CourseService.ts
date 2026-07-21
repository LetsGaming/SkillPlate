import { BaseService } from '@/services/base/BaseService';
import ApiUtils from '@/utils/ApiUtils';

const BASE_ENDPOINT = '/course';
const RESOURCE_KEY = 'course.title';

export default class CourseService extends BaseService {
  /**
   * Fetches a single course by ID.
   * GET /api/course/:id
   */
  static async getCourse(id: string): Promise<{ courseId: string }> {
    return this.handleRequest(
      ApiUtils.get<{ courseId: string }>(`${BASE_ENDPOINT}/${id}`),
      RESOURCE_KEY,
      'course.fetch_failed',
    );
  }

  /**
   * Generates a new course via the AI (Ollama) backend.
   * POST /api/course/:theme/:difficulty/:duration/:online
   *
   * The backend URL shape is positional path params, so we build the path here.
   */
  static async generateCourse(params: CourseGenerateParams): Promise<Course> {
    const { theme, difficulty, duration, online } = params;
    const path = `${BASE_ENDPOINT}/${encodeURIComponent(theme)}/${encodeURIComponent(difficulty)}/${duration}/${online}`;

    const response = await this.handleRequest<CourseResponseData>(
      ApiUtils.post(path, null),
      RESOURCE_KEY,
      'course.generate_failed',
    );

    return response.course;
  }
}
