const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api"

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  email: string
  username: string
  first_name: string
  last_name: string
  password: string
  password_confirm: string
  user_type: "student" | "instructor"
}

export interface User {
  id: string
  email: string
  username: string
  first_name: string
  last_name: string
  user_type: string
  avatar?: string
  is_verified: boolean
  country?: string
  city?: string
  bio?: string
}

export interface AuthResponse {
  access: string
  refresh: string
  user: User
}

class AuthService {
  private getAuthHeaders() {
    const token = localStorage.getItem("access_token")
    return {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` }),
    }
  }

  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await fetch(`${API_BASE_URL}/auth/login/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(credentials),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || "Login failed")
    }

    const data = await response.json()

    // Store tokens and user info
    localStorage.setItem("access_token", data.access)
    localStorage.setItem("refresh_token", data.refresh)
    localStorage.setItem("user", JSON.stringify(data.user))

    return data
  }

  async register(userData: RegisterData): Promise<{ message: string }> {
    const response = await fetch(`${API_BASE_URL}/auth/register/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userData),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(Object.values(error).flat().join(", "))
    }

    return await response.json()
  }

  async getCurrentUser(): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/auth/profile/`, {
      headers: this.getAuthHeaders(),
    })

    if (!response.ok) {
      throw new Error("Failed to get user profile")
    }

    const user = await response.json()
    localStorage.setItem("user", JSON.stringify(user))
    return user
  }

  async updateProfile(userData: Partial<User>): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/auth/profile/`, {
      method: "PATCH",
      headers: this.getAuthHeaders(),
      body: JSON.stringify(userData),
    })

    if (!response.ok) {
      throw new Error("Failed to update profile")
    }

    const user = await response.json()
    localStorage.setItem("user", JSON.stringify(user))
    return user
  }

  async refreshToken(): Promise<string> {
    const refreshToken = localStorage.getItem("refresh_token")
    if (!refreshToken) {
      throw new Error("No refresh token available")
    }

    const response = await fetch(`${API_BASE_URL}/auth/refresh/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh: refreshToken }),
    })

    if (!response.ok) {
      throw new Error("Token refresh failed")
    }

    const data = await response.json()
    localStorage.setItem("access_token", data.access)
    return data.access
  }

  logout() {
    localStorage.removeItem("access_token")
    localStorage.removeItem("refresh_token")
    localStorage.removeItem("user")
  }

  isAuthenticated(): boolean {
    return !!localStorage.getItem("access_token")
  }

  getCurrentUserFromStorage(): User | null {
    const userStr = localStorage.getItem("user")
    return userStr ? JSON.parse(userStr) : null
  }

  getUserRole(): string | null {
    const user = this.getCurrentUserFromStorage()
    return user?.user_type || null
  }
}

export const authService = new AuthService()