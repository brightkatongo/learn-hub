"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { BookOpen, Users, DollarSign, Plus, Edit, Eye, BarChart3, Star, Settings, LogOut } from "lucide-react"
import Link from "next/link"
import { useRouter } from "next/navigation"

export default function InstructorDashboard() {
  const [user, setUser] = useState({
    name: "Sarah Johnson",
    email: "sarah@example.com",
    avatar: "/placeholder.svg?height=40&width=40",
    userType: "instructor",
  })
  const router = useRouter()

  useEffect(() => {
    // Check if user is authenticated and is an instructor
    const token = localStorage.getItem("access_token")
    if (!token) {
      router.push("/login")
    }
  }, [router])

  const handleLogout = () => {
    localStorage.removeItem("access_token")
    router.push("/")
  }

  const instructorCourses = [
    {
      id: 1,
      title: "Complete React Developer Course",
      students: 12543,
      rating: 4.8,
      reviews: 2543,
      revenue: 125430,
      status: "Published",
      thumbnail: "/placeholder.svg?height=100&width=150",
      lastUpdated: "Dec 15, 2024",
    },
    {
      id: 2,
      title: "Advanced React Patterns",
      students: 3421,
      rating: 4.9,
      reviews: 876,
      revenue: 34210,
      status: "Published",
      thumbnail: "/placeholder.svg?height=100&width=150",
      lastUpdated: "Dec 10, 2024",
    },
    {
      id: 3,
      title: "React Testing Fundamentals",
      students: 0,
      rating: 0,
      reviews: 0,
      revenue: 0,
      status: "Draft",
      thumbnail: "/placeholder.svg?height=100&width=150",
      lastUpdated: "Dec 20, 2024",
    },
  ]

  const recentActivity = [
    { type: "enrollment", message: "New student enrolled in React Course", time: "2 hours ago" },
    { type: "review", message: "New 5-star review received", time: "4 hours ago" },
    { type: "question", message: "Student asked a question in Chapter 5", time: "6 hours ago" },
    { type: "completion", message: "Student completed your course", time: "1 day ago" },
  ]

  const stats = {
    totalStudents: 15964,
    totalRevenue: 159640,
    totalCourses: 3,
    avgRating: 4.85,
  }

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
                <Settings className="h-4 w-4" />
              </Button>
              <div className="flex items-center space-x-2">
                <Avatar className="h-8 w-8">
                  <AvatarImage src={user.avatar || "/placeholder.svg"} />
                  <AvatarFallback>SJ</AvatarFallback>
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
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Instructor Dashboard</h1>
          <p className="text-gray-600">Manage your courses and track your teaching performance</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <Users className="h-8 w-8 text-blue-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Total Students</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.totalStudents.toLocaleString()}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <DollarSign className="h-8 w-8 text-green-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Total Revenue</p>
                  <p className="text-2xl font-bold text-gray-900">${stats.totalRevenue.toLocaleString()}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <BookOpen className="h-8 w-8 text-purple-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Total Courses</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.totalCourses}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <Star className="h-8 w-8 text-yellow-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Avg. Rating</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.avgRating}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <Tabs defaultValue="courses" className="space-y-6">
          <TabsList>
            <TabsTrigger value="courses">My Courses</TabsTrigger>
            <TabsTrigger value="analytics">Analytics</TabsTrigger>
            <TabsTrigger value="students">Students</TabsTrigger>
            <TabsTrigger value="reviews">Reviews</TabsTrigger>
          </TabsList>

          <TabsContent value="courses" className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold">My Courses</h2>
              <Button>
                <Plus className="mr-2 h-4 w-4" />
                Create New Course
              </Button>
            </div>

            <div className="grid gap-6">
              {instructorCourses.map((course) => (
                <Card key={course.id}>
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
                            <div className="flex items-center gap-2 mb-2">
                              <h3 className="text-xl font-semibold">{course.title}</h3>
                              <Badge variant={course.status === "Published" ? "default" : "secondary"}>
                                {course.status}
                              </Badge>
                            </div>

                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                              <div>
                                <p className="text-sm text-gray-600">Students</p>
                                <p className="font-semibold">{course.students.toLocaleString()}</p>
                              </div>
                              <div>
                                <p className="text-sm text-gray-600">Rating</p>
                                <div className="flex items-center">
                                  <Star className="w-4 h-4 fill-yellow-400 text-yellow-400 mr-1" />
                                  <span className="font-semibold">{course.rating}</span>
                                  <span className="text-sm text-gray-600 ml-1">({course.reviews})</span>
                                </div>
                              </div>
                              <div>
                                <p className="text-sm text-gray-600">Revenue</p>
                                <p className="font-semibold">${course.revenue.toLocaleString()}</p>
                              </div>
                              <div>
                                <p className="text-sm text-gray-600">Last Updated</p>
                                <p className="font-semibold">{course.lastUpdated}</p>
                              </div>
                            </div>

                            <div className="flex gap-2">
                              <Button size="sm" variant="outline">
                                <Edit className="mr-2 h-4 w-4" />
                                Edit
                              </Button>
                              <Button size="sm" variant="outline">
                                <Eye className="mr-2 h-4 w-4" />
                                Preview
                              </Button>
                              <Button size="sm" variant="outline">
                                <BarChart3 className="mr-2 h-4 w-4" />
                                Analytics
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

          <TabsContent value="analytics" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Performance Analytics</CardTitle>
                <CardDescription>Track your teaching performance and student engagement</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-blue-600 mb-2">1,234</div>
                    <div className="text-sm text-gray-600">New Students This Month</div>
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-green-600 mb-2">$12,450</div>
                    <div className="text-sm text-gray-600">Revenue This Month</div>
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-purple-600 mb-2">89%</div>
                    <div className="text-sm text-gray-600">Course Completion Rate</div>
                  </div>
                </div>

                <div className="h-64 bg-gray-100 rounded-lg flex items-center justify-center">
                  <div className="text-center">
                    <BarChart3 className="h-12 w-12 text-gray-400 mx-auto mb-2" />
                    <p className="text-gray-500">Analytics charts would be displayed here</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="students" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Student Management</CardTitle>
                <CardDescription>View and manage your students</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="text-center py-8">
                    <Users className="h-12 w-12 text-gray-400 mx-auto mb-2" />
                    <p className="text-gray-500">Student management features would be displayed here</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="reviews" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Recent Reviews</CardTitle>
                <CardDescription>See what your students are saying about your courses</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="border-b pb-4">
                    <div className="flex items-start space-x-4">
                      <Avatar>
                        <AvatarImage src="/placeholder.svg?height=40&width=40" />
                        <AvatarFallback>JD</AvatarFallback>
                      </Avatar>
                      <div className="flex-1">
                        <div className="flex items-center justify-between mb-2">
                          <h4 className="font-semibold">John Doe</h4>
                          <span className="text-sm text-gray-500">2 days ago</span>
                        </div>
                        <div className="flex items-center mb-2">
                          {[...Array(5)].map((_, i) => (
                            <Star key={i} className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                          ))}
                        </div>
                        <p className="text-sm text-gray-600">
                          "Excellent course! Sarah explains everything clearly and the projects are very practical."
                        </p>
                        <p className="text-xs text-gray-500 mt-1">Complete React Developer Course</p>
                      </div>
                    </div>
                  </div>

                  <div className="border-b pb-4">
                    <div className="flex items-start space-x-4">
                      <Avatar>
                        <AvatarImage src="/placeholder.svg?height=40&width=40" />
                        <AvatarFallback>JS</AvatarFallback>
                      </Avatar>
                      <div className="flex-1">
                        <div className="flex items-center justify-between mb-2">
                          <h4 className="font-semibold">Jane Smith</h4>
                          <span className="text-sm text-gray-500">1 week ago</span>
                        </div>
                        <div className="flex items-center mb-2">
                          {[...Array(4)].map((_, i) => (
                            <Star key={i} className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                          ))}
                          <Star className="w-4 h-4 text-gray-300" />
                        </div>
                        <p className="text-sm text-gray-600">
                          "Great content and well-structured. The instructor is knowledgeable."
                        </p>
                        <p className="text-xs text-gray-500 mt-1">Advanced React Patterns</p>
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        {/* Recent Activity */}
        <Card className="mt-8">
          <CardHeader>
            <CardTitle>Recent Activity</CardTitle>
            <CardDescription>Stay updated with the latest activities in your courses</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentActivity.map((activity, index) => (
                <div key={index} className="flex items-center space-x-4 p-3 bg-gray-50 rounded-lg">
                  <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                  <div className="flex-1">
                    <p className="text-sm">{activity.message}</p>
                    <p className="text-xs text-gray-500">{activity.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
