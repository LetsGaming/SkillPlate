// --- Auth ---

interface LoginData {
  username: string;
  password: string;
}

/** Backend returns { access_token: string } inside the data envelope */
interface LoginResponseData {
  access_token: string;
}

type UserRole = 'admin' | 'user' | 'guest';

interface AuthToken {
  id: number;
  username: string;
  role: UserRole;
}

// --- Course ---

interface Ingredient {
  ingredient_name: string;
  ingredient_type: string;
  amount: number;
  unit: string;
}

interface Recipe {
  recipe_name: string;
  recipe_instructions: string;
  ingredients: Ingredient[];
}

interface Course {
  theme: string;
  difficulty: string;
  duration: number;
  online: boolean;
  recipes: Recipe[];
}

interface CourseResponseData {
  course: Course;
}

interface CourseGenerateParams {
  theme: string;
  difficulty: string;
  duration: number;
  online: boolean;
}
