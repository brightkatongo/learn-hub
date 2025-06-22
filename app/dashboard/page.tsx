"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
  BookOpen,
  Clock,
  Award,
  TrendingUp,
  Play,
  Calendar,
  Bell,
  Settings,
  LogOut,
  BarChart3,
  PlusCircle,
} from "lucide-react"
import Link from "next/link"
import { useRouter } from "next/navigation"

export default function DashboardPage() {
  const [user, setUser] = useState({
    name: "John Doe",
    email: "john@example.com",
    avatar: "/placeholder.svg?height=40&width=40",
    userType: "student",
  })
  const router = useRouter()

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem("access_token")
    if (!token) {
      router.push("/login")
    }
  }, [router])

  const handleLogout = () => {
    localStorage.removeItem("access_token")
    router.push("/")
  }

  const enrolledCourses = [
    {
      id: 1,
      title: "Complete React Developer Course",
      instructor: "Sarah Johnson",
      progress: 65,
      totalLessons: 45,
      completedLessons: 29,
      thumbnail: "/placeholder.svg?height=100&width=150",
      lastAccessed: "2 hours ago",
    },
    {
      id: 2,
      title: "Machine Learning Fundamentals",
      instructor: "Dr. Michael Chen",
      progress: 30,
      totalLessons: 38,
      completedLessons: 11,
      thumbnail: "/placeholder.svg?height=100&width=150",
      lastAccessed: "1 day ago",
    },
    {
      id: 3,
      title: "UI/UX Design Principles",
      instructor: "Emma Rodriguez",
      progress: 85,
      totalLessons: 25,
      completedLessons: 21,
      thumbnail: "/placeholder.svg?height=100&width=150",
      lastAccessed: "3 hours ago",
    },
  ]

  const achievements = [
    { title: "First Course Completed", icon: "🎓", date: "Dec 15, 2024" },
    { title: "Week Streak", icon: "🔥", date: "Dec 10, 2024" },
    { title: "Quiz Master", icon: "🧠", date: "Dec 5, 2024" },
  ]

  const upcomingDeadlines = [
    { course: "React Course", task: "Final Project", due: "Dec 25, 2024" },
    { course: "ML Course", task: "Assignment 3", due: "Dec 28, 2024" },
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Link href="/" className="text-2xl font-bold text-primary">
              LearnHub
            </Link>

            <div className="flex items-center space-x-4">
              <Button variant="ghost" size="sm">
                <Bell className="h-4 w-4" />
              </Button>
              <Button variant="ghost" size="sm">
                <Settings className="h-4 w-4" />
              </Button>
              <div className="flex items-center space-x-2">
                <Avatar className="h-8 w-8">
                  <AvatarImage src={user.avatar || "/placeholder.svg"} />
                  <AvatarFallback>JD</AvatarFallback>
                </Avatar>
                <span className="text-sm font-medium">{user.name}</span>
              </div>
              <Button variant="ghost" size="sm" onClick={handleLogout}>
                <LogOut className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Welcome back, {user.name}!</h1>
          <p className="text-gray-600">Continue your learning journey</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <BookOpen className="h-8 w-8 text-blue-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Enrolled Courses</p>
                  <p className="text-2xl font-bold text-gray-900">3</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <Clock className="h-8 w-8 text-green-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Hours Learned</p>
                  <p className="text-2xl font-bold text-gray-900">47</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <Award className="h-8 w-8 text-yellow-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Certificates</p>
                  <p className="text-2xl font-bold text-gray-900">1</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <TrendingUp className="h-8 w-8 text-purple-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Avg. Progress</p>
                  <p className="text-2xl font-bold text-gray-900">60%</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <Tabs defaultValue="courses" className="space-y-6">
          <TabsList>
            <TabsTrigger value="courses">My Courses</TabsTrigger>
            <TabsTrigger value="progress">Progress</TabsTrigger>
            <TabsTrigger value="achievements">Achievements</TabsTrigger>
            <TabsTrigger value="schedule">Schedule</TabsTrigger>
          </TabsList>

          <TabsContent value="courses" className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold">My Courses</h2>
              <Button asChild>
                <Link href="/courses">
                  <PlusCircle className="mr-2 h-4 w-4" />
                  Browse Courses
                </Link>
              </Button>
            </div>

            <div className="grid gap-6">
              {enrolledCourses.map((course) => (
                <Card key={course.id} className="overflow-hidden">
                  <CardContent className="p-0">
                    <div className="flex">
                      <div className="w-48 h-32 bg-gray-200 flex-shrink-0">
                        <img
                          src={course.thumbnail || "/placeholder.svg"}
                          alt={course.title}
                          className="w-full h-full object-cover"
                        />
                      </div>
                      <div className="flex-1 p-6">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <h3 className="text-xl font-semibold mb-2">{course.title}</h3>
                            <p className="text-gray-600 mb-4">by {course.instructor}</p>

                            <div className="space-y-2 mb-4">
                              <div className="flex items-center justify-between text-sm">
                                <span>Progress</span>
                                <span>{course.progress}%</span>
                              </div>
                              <Progress value={course.progress} className="h-2" />
                              <p className="text-sm text-gray-600">
                                {course.completedLessons} of {course.totalLessons} lessons completed
                              </p>
                            </div>

                            <div className="flex items-center justify-between">
                              <span className="text-sm text-gray-500">Last accessed {course.lastAccessed}</span>
                              <Button size="sm">
                                <Play className="mr-2 h-4 w-4" />
                                Continue Learning
                              </Button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="progress" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Learning Progress</CardTitle>
                <CardDescription>Your learning statistics and progress over time</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="text-center">
                      <div className="text-3xl font-bold text-blue-600 mb-2">47</div>
                      <div className="text-sm text-gray-600">Hours This Month</div>
                    </div>
                    <div className="text-center">
                      <div className="text-3xl font-bold text-green-600 mb-2">12</div>
                      <div className="text-sm text-gray-600">Lessons Completed</div>
                    </div>
                    <div className="text-center">
                      <div className="text-3xl font-bold text-purple-600 mb-2">7</div>
                      <div className="text-sm text-gray-600">Day Streak</div>
                    </div>
                  </div>

                  <div className="h-64 bg-gray-100 rounded-lg flex items-center justify-center">
                    <div className="text-center">
                      <BarChart3 className="h-12 w-12 text-gray-400 mx-auto mb-2" />
                      <p className="text-gray-500">Progress chart would be displayed here</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="achievements" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Achievements</CardTitle>
                <CardDescription>Your learning milestones and accomplishments</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid gap-4">
                  {achievements.map((achievement, index) => (
                    <div key={index} className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg">
                      <div className="text-2xl">{achievement.icon}</div>
                      <div className="flex-1">
                        <h3 className="font-semibold">{achievement.title}</h3>
                        <p className="text-sm text-gray-600">Earned on {achievement.date}</p>
                      </div>
                      <Badge variant="secondary">Completed</Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="schedule" className="space-y-6">
            <div className="grid lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Upcoming Deadlines</CardTitle>
                  <CardDescription>Don't miss these important dates</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {upcomingDeadlines.map((deadline, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg">
                        <div>
                          <h4 className="font-medium">{deadline.task}</h4>
                          <p className="text-sm text-gray-600">{deadline.course}</p>
                        </div>
                        <div className="text-right">
                          <p className="text-sm font-medium text-yellow-700">Due {deadline.due}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Study Schedule</CardTitle>
                  <CardDescription>Your planned learning sessions</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center space-x-4 p-3 border rounded-lg">
                      <Calendar className="h-5 w-5 text-blue-600" />
                      <div>
                        <h4 className="font-medium">React Course - Chapter 5</h4>
                        <p className="text-sm text-gray-600">Today, 2:00 PM - 3:30 PM</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-4 p-3 border rounded-lg">
                      <Calendar className="h-5 w-5 text-green-600" />
                      <div>
                        <h4 className="font-medium">ML Assignment Review</h4>
                        <p className="text-sm text-gray-600">Tomorrow, 10:00 AM - 11:00 AM</p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
