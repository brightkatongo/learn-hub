"use client"

import type React from "react"

import { createContext, useContext, useEffect, useState } from "react"
import { authService, type User } from "@/app/api/auth"

interface AuthContextType {
  user: User | null
  loading: boolean
  signIn: (email: string, password: string) => Promise<any>
  signUp: (email: string, password: string, userData: any) => Promise<any>
  signOut: () => Promise<void>
  updateProfile: (data: any) => Promise<any>
  isAuthenticated: boolean
  userRole: string | null
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check if user is already logged in
    const initAuth = async () => {
      try {
        if (authService.isAuthenticated()) {
          const currentUser = await authService.getCurrentUser()
          setUser(currentUser)
        }
      } catch (error) {
        console.error("Auth initialization error:", error)
        authService.logout()
      } finally {
        setLoading(false)
      }
    }

    initAuth()
  }, [])

  const signIn = async (email: string, password: string) => {
    try {
      const response = await authService.login({ email, password })
      setUser(response.user)
      return { data: response, error: null }
    } catch (error) {
      return { data: null, error }
    }
  }

  const signUp = async (email: string, password: string, userData: any) => {
    try {
      const response = await authService.register({
        email,
        password,
        password_confirm: password,
        ...userData,
      })
      return { data: response, error: null }
    } catch (error) {
      return { data: null, error }
    }
  }

  const signOut = async () => {
    authService.logout()
    setUser(null)
  }

  const updateProfile = async (updates: any) => {
    try {
      const updatedUser = await authService.updateProfile(updates)
      setUser(updatedUser)
      return { data: updatedUser, error: null }
    } catch (error) {
      return { data: null, error }
    }
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        signIn,
        signUp,
        signOut,
        updateProfile,
        isAuthenticated: !!user,
        userRole: user?.user_type || null,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}