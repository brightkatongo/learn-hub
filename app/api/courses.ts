const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api"

export interface Course {
  id: string
  title: string
  subtitle: string
  description: string
  instructor_name: string
  category_name: string
  thumbnail?: string
  price: number
  original_price?: number
  is_free: boolean
  difficulty_level: string
  language: string
  is_bestseller: boolean
  is_featured: boolean
  total_duration: number
  total_lectures: number
  average_rating: number
  total_students: number
  created_at: string
  updated_at: string
}

export interface CourseDetail extends Course {
  instructor: any
  category: any
  sections: Section[]
  reviews_count: number
  requirements: string[]
  what_you_will_learn: string[]
  target_audience: string[]
}

export interface Section {
  id: number
  title: string
  description: string
  lectures: Lecture[]
  lecture_count: number
  total_duration: number
  order: number
}

export interface Lecture {
  id: string
  title: string
  description: string
  lecture_type: string
  video_duration: number
  order: number
  is_preview: boolean
  is_free: boolean
}

export interface Enrollment {
  id: string
  course: Course
  enrolled_at: string
  progress_percentage: number
  completed: boolean
  time_spent: number
  last_accessed: string
}

class CourseService {
  private getAuthHeaders() {
    const token = localStorage.getItem("access_token")
    return {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` }),
    }
  }

  async getCourses(params?: {
    search?: string
    category?: string
    difficulty_level?: string
    is_free?: boolean
    ordering?: string
  }): Promise<{ results: Course[]; count: number }> {
    const searchParams = new URLSearchParams()
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          searchParams.append(key, value.toString())
        }
      })
    }

    const response = await fetch(`${API_BASE_URL}/courses/?${searchParams}`)
    if (!response.ok) {
      throw new Error("Failed to fetch courses")
    }

    return await response.json()
  }

  async getCourse(id: string): Promise<CourseDetail> {
    const response = await fetch(`${API_BASE_URL}/courses/${id}/`)
    if (!response.ok) {
      throw new Error("Failed to fetch course")
    }

    return await response.json()
  }

  async getFeaturedCourses(): Promise<Course[]> {
    const response = await fetch(`${API_BASE_URL}/courses/featured/`)
    if (!response.ok) {
      throw new Error("Failed to fetch featured courses")
    }

    return await response.json()
  }

  async getPopularCourses(): Promise<Course[]> {
    const response = await fetch(`${API_BASE_URL}/courses/popular/`)
    if (!response.ok) {
      throw new Error("Failed to fetch popular courses")
    }

    return await response.json()
  }

  async enrollInCourse(courseId: string): Promise<Enrollment> {
    const response = await fetch(`${API_BASE_URL}/courses/enroll/${courseId}/`, {
      method: "POST",
      headers: this.getAuthHeaders(),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error || "Failed to enroll in course")
    }

    return await response.json()
  }

  async getMyEnrollments(): Promise<Enrollment[]> {
    const response = await fetch(`${API_BASE_URL}/courses/enrollments/`, {
      headers: this.getAuthHeaders(),
    })

    if (!response.ok) {
      throw new Error("Failed to fetch enrollments")
    }

    const data = await response.json()
    return data.results || data
  }

  async getInstructorCourses(): Promise<Course[]> {
    const response = await fetch(`${API_BASE_URL}/courses/instructor/courses/`, {
      headers: this.getAuthHeaders(),
    })

    if (!response.ok) {
      throw new Error("Failed to fetch instructor courses")
    }

    const data = await response.json()
    return data.results || data
  }

  async createCourse(courseData: Partial<Course>): Promise<Course> {
    const response = await fetch(`${API_BASE_URL}/courses/instructor/courses/`, {
      method: "POST",
      headers: this.getAuthHeaders(),
      body: JSON.stringify(courseData),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(Object.values(error).flat().join(", "))
    }

    return await response.json()
  }

  async searchCourses(
    query: string,
    filters?: {
      category?: string
      level?: string
      price_range?: string
    },
  ): Promise<Course[]> {
    const searchParams = new URLSearchParams({ q: query })
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value) {
          searchParams.append(key, value)
        }
      })
    }

    const response = await fetch(`${API_BASE_URL}/courses/search/?${searchParams}`)
    if (!response.ok) {
      throw new Error("Failed to search courses")
    }

    return await response.json()
  }
}

export const courseService = new CourseService()
