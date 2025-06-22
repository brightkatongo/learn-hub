import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Upload, Video, Users, DollarSign, TrendingUp, Eye, Star, Edit, Trash2, Plus } from "lucide-react"
import Link from "next/link"
import Image from "next/image"

export default function InstructorDashboard() {
  const instructorStats = {
    totalStudents: 15420,
    totalRevenue: 45680,
    totalCourses: 8,
    averageRating: 4.7,
    monthlyEarnings: 8950,
    newEnrollments: 234,
  }

  const courses = [
    {
      id: 1,
      title: "Complete React Developer Course",
      status: "Published",
      students: 12543,
      rating: 4.8,
      revenue: 18500,
      lastUpdated: "2 days ago",
      image: "/placeholder.svg?height=100&width=150",
    },
    {
      id: 2,
      title: "Advanced JavaScript Concepts",
      status: "Draft",
      students: 0,
      rating: 0,
      revenue: 0,
      lastUpdated: "1 week ago",
      image: "/placeholder.svg?height=100&width=150",
    },
    {
      id: 3,
      title: "Node.js Backend Development",
      status: "Published",
      students: 2877,
      rating: 4.6,
      revenue: 12300,
      lastUpdated: "5 days ago",
      image: "/placeholder.svg?height=100&width=150",
    },
  ]

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-white sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Link href="/" className="text-2xl font-bold text-primary">
              LearnHub
            </Link>
            <div className="flex items-center space-x-4">
              <Button variant="outline" asChild>
                <Link href="/courses">Student View</Link>
              </Button>
              <Button asChild>
                <Link href="/instructor/course/new">
                  <Plus className="w-4 h-4 mr-2" />
                  Create Course
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Instructor Dashboard</h1>
          <p className="text-muted-foreground">Manage your courses and track your teaching success</p>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
          <Card>
            <CardContent className="p-4 text-center">
              <Users className="w-8 h-8 mx-auto mb-2 text-blue-500" />
              <div className="text-2xl font-bold">{instructorStats.totalStudents.toLocaleString()}</div>
              <div className="text-xs text-muted-foreground">Total Students</div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4 text-center">
              <DollarSign className="w-8 h-8 mx-auto mb-2 text-green-500" />
              <div className="text-2xl font-bold">${instructorStats.totalRevenue.toLocaleString()}</div>
              <div className="text-xs text-muted-foreground">Total Revenue</div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4 text-center">
              <Video className="w-8 h-8 mx-auto mb-2 text-purple-500" />
              <div className="text-2xl font-bold">{instructorStats.totalCourses}</div>
              <div className="text-xs text-muted-foreground">Total Courses</div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4 text-center">
              <Star className="w-8 h-8 mx-auto mb-2 text-yellow-500" />
              <div className="text-2xl font-bold">{instructorStats.averageRating}</div>
              <div className="text-xs text-muted-foreground">Avg Rating</div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4 text-center">
              <TrendingUp className="w-8 h-8 mx-auto mb-2 text-orange-500" />
              <div className="text-2xl font-bold">${instructorStats.monthlyEarnings.toLocaleString()}</div>
              <div className="text-xs text-muted-foreground">This Month</div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4 text-center">
              <Eye className="w-8 h-8 mx-auto mb-2 text-red-500" />
              <div className="text-2xl font-bold">{instructorStats.newEnrollments}</div>
              <div className="text-xs text-muted-foreground">New This Week</div>
            </CardContent>
          </Card>
        </div>

        <Tabs defaultValue="courses" className="w-full">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="courses">My Courses</TabsTrigger>
            <TabsTrigger value="create">Create Course</TabsTrigger>
            <TabsTrigger value="analytics">Analytics</TabsTrigger>
            <TabsTrigger value="earnings">Earnings</TabsTrigger>
          </TabsList>

          <TabsContent value="courses" className="space-y-4">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-semibold">Your Courses</h2>
              <Button asChild>
                <Link href="/instructor/course/new">
                  <Plus className="w-4 h-4 mr-2" />
                  New Course
                </Link>
              </Button>
            </div>

            <div className="space-y-4">
              {courses.map((course) => (
                <Card key={course.id}>
                  <CardContent className="p-0">
                    <div className="flex">
                      <Image
                        src={course.image || "/placeholder.svg"}
                        alt={course.title}
                        width={150}
                        height={100}
                        className="object-cover"
                      />
                      <div className="flex-1 p-4">
                        <div className="flex justify-between items-start mb-2">
                          <div>
                            <h3 className="font-semibold mb-1">{course.title}</h3>
                            <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                              <Badge variant={course.status === "Published" ? "default" : "secondary"}>
                                {course.status}
                              </Badge>
                              <span>Updated {course.lastUpdated}</span>
                            </div>
                          </div>
                          <div className="flex space-x-2">
                            <Button size="sm" variant="outline">
                              <Edit className="w-4 h-4 mr-2" />
                              Edit
                            </Button>
                            <Button size="sm" variant="outline">
                              <Eye className="w-4 h-4 mr-2" />
                              Preview
                            </Button>
                            <Button size="sm" variant="outline" className="text-red-600">
                              <Trash2 className="w-4 h-4" />
                            </Button>
                          </div>
                        </div>

                        <div className="grid grid-cols-4 gap-4 text-sm">
                          <div>
                            <div className="font-semibold">{course.students.toLocaleString()}</div>
                            <div className="text-muted-foreground">Students</div>
                          </div>
                          <div>
                            <div className="font-semibold flex items-center">
                              <Star className="w-4 h-4 fill-yellow-400 text-yellow-400 mr-1" />
                              {course.rating || "N/A"}
                            </div>
                            <div className="text-muted-foreground">Rating</div>
                          </div>
                          <div>
                            <div className="font-semibold">${course.revenue.toLocaleString()}</div>
                            <div className="text-muted-foreground">Revenue</div>
                          </div>
                          <div>
                            <Button size="sm" className="w-full" asChild>
                              <Link href={`/instructor/courses/${course.id}`}>Manage</Link>
                            </Button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="create" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Create New Course</CardTitle>
                <CardDescription>Fill in the basic information to get started with your new course</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="title">Course Title</Label>
                    <Input id="title" placeholder="Enter course title" />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="category">Category</Label>
                    <Select>
                      <SelectTrigger>
                        <SelectValue placeholder="Select category" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="web-dev">Web Development</SelectItem>
                        <SelectItem value="data-science">Data Science</SelectItem>
                        <SelectItem value="design">Design</SelectItem>
                        <SelectItem value="business">Business</SelectItem>
                        <SelectItem value="marketing">Marketing</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="description">Course Description</Label>
                  <Textarea id="description" placeholder="Describe what students will learn in this course" rows={4} />
                </div>

                <div className="grid md:grid-cols-3 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="level">Difficulty Level</Label>
                    <Select>
                      <SelectTrigger>
                        <SelectValue placeholder="Select level" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="beginner">Beginner</SelectItem>
                        <SelectItem value="intermediate">Intermediate</SelectItem>
                        <SelectItem value="advanced">Advanced</SelectItem>
                        <SelectItem value="all">All Levels</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="language">Language</Label>
                    <Select>
                      <SelectTrigger>
                        <SelectValue placeholder="Select language" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="english">English</SelectItem>
                        <SelectItem value="spanish">Spanish</SelectItem>
                        <SelectItem value="french">French</SelectItem>
                        <SelectItem value="german">German</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="price">Price ($)</Label>
                    <Input id="price" type="number" placeholder="0.00" />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label>Course Thumbnail</Label>
                  <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                    <Upload className="w-12 h-12 mx-auto mb-4 text-gray-400" />
                    <p className="text-sm text-muted-foreground mb-2">Upload course thumbnail (1280x720 recommended)</p>
                    <Button variant="outline" size="sm">
                      Choose File
                    </Button>
                  </div>
                </div>

                <div className="flex space-x-4">
                  <Button>Create Course</Button>
                  <Button variant="outline">Save as Draft</Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="analytics" className="space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Student Enrollment Trends</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="h-64 flex items-center justify-center text-muted-foreground">
                    📈 Enrollment chart would go here
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Revenue Analytics</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="h-64 flex items-center justify-center text-muted-foreground">
                    💰 Revenue chart would go here
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Course Performance</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {courses
                      .filter((c) => c.status === "Published")
                      .map((course) => (
                        <div key={course.id} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                          <div>
                            <h4 className="font-medium">{course.title}</h4>
                            <p className="text-sm text-muted-foreground">
                              {course.students} students • {course.rating} rating
                            </p>
                          </div>
                          <div className="text-right">
                            <div className="font-semibold">${course.revenue.toLocaleString()}</div>
                            <div className="text-sm text-muted-foreground">Revenue</div>
                          </div>
                        </div>
                      ))}
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Student Feedback</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm">5 stars</span>
                      <div className="flex-1 mx-3 bg-gray-200 rounded-full h-2">
                        <div className="bg-yellow-400 h-2 rounded-full" style={{ width: "75%" }}></div>
                      </div>
                      <span className="text-sm">75%</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm">4 stars</span>
                      <div className="flex-1 mx-3 bg-gray-200 rounded-full h-2">
                        <div className="bg-yellow-400 h-2 rounded-full" style={{ width: "20%" }}></div>
                      </div>
                      <span className="text-sm">20%</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm">3 stars</span>
                      <div className="flex-1 mx-3 bg-gray-200 rounded-full h-2">
                        <div className="bg-yellow-400 h-2 rounded-full" style={{ width: "3%" }}></div>
                      </div>
                      <span className="text-sm">3%</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm">2 stars</span>
                      <div className="flex-1 mx-3 bg-gray-200 rounded-full h-2">
                        <div className="bg-yellow-400 h-2 rounded-full" style={{ width: "1%" }}></div>
                      </div>
                      <span className="text-sm">1%</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm">1 star</span>
                      <div className="flex-1 mx-3 bg-gray-200 rounded-full h-2">
                        <div className="bg-yellow-400 h-2 rounded-full" style={{ width: "1%" }}></div>
                      </div>
                      <span className="text-sm">1%</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="earnings" className="space-y-6">
            <div className="grid md:grid-cols-3 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>This Month</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-green-600 mb-2">
                    ${instructorStats.monthlyEarnings.toLocaleString()}
                  </div>
                  <p className="text-sm text-muted-foreground">+15% from last month</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Total Earnings</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold mb-2">${instructorStats.totalRevenue.toLocaleString()}</div>
                  <p className="text-sm text-muted-foreground">All time earnings</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Pending Payout</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-orange-600 mb-2">$2,450</div>
                  <p className="text-sm text-muted-foreground">Available Dec 30</p>
                </CardContent>
              </Card>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>Recent Transactions</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {[
                    {
                      course: "Complete React Developer Course",
                      amount: 89.99,
                      date: "Dec 21, 2024",
                      student: "John Doe",
                    },
                    {
                      course: "Node.js Backend Development",
                      amount: 79.99,
                      date: "Dec 21, 2024",
                      student: "Jane Smith",
                    },
                    {
                      course: "Complete React Developer Course",
                      amount: 89.99,
                      date: "Dec 20, 2024",
                      student: "Mike Johnson",
                    },
                    {
                      course: "Node.js Backend Development",
                      amount: 79.99,
                      date: "Dec 20, 2024",
                      student: "Sarah Wilson",
                    },
                  ].map((transaction, index) => (
                    <div key={index} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                      <div>
                        <h4 className="font-medium">{transaction.course}</h4>
                        <p className="text-sm text-muted-foreground">
                          Purchased by {transaction.student} on {transaction.date}
                        </p>
                      </div>
                      <div className="text-right">
                        <div className="font-semibold text-green-600">+${transaction.amount}</div>
                        <div className="text-xs text-muted-foreground">
                          Your share: ${(transaction.amount * 0.7).toFixed(2)}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
