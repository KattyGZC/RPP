export interface UserProfile {
  role: "student" | "teacher" | "admin";
  birth_date: string | null;
  photo: string | null;
}

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  profile: UserProfile;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  password: string;
  password_confirm: string;
  first_name: string;
  last_name: string;
  email?: string;
  birth_date?: string;
  role?: "student" | "teacher";
}

export interface UpdateProfileData {
  first_name?: string;
  last_name?: string;
  birth_date?: string;
  photo?: File;
}
