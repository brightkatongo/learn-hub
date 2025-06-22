import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
  Star,
  Users,
  Clock,
  Play,
  Download,
  Share2,
  Heart,
  CheckCircle,
  Globe,
  Award,
  Smartphone,
  Infinity,
} from "lucide-react"
import Link from "next/link"
import Image from "next/image"

export default function CourseDetailPage() {
  const course = {
    id: 1,
    title: "Complete React Developer Course",
    subtitle: "Learn React from scratch and build amazing web applications",
    instructor: {
      name: "Sarah Johnson",
      title: "Senior Full Stack Developer",
      avatar: "/placeholder.svg?height=100&width=100",
      rating: 4.8,
      students: 45000,
      courses: 12,
    },
    rating: 4.8,
    reviews: 2543,
    students: 12543,
    duration: "42 hours",
    lectures: 156,
    price: 89.99,
    originalPrice: 199.99,
    image: "/placeholder.svg?height=400&width=600",
    category: "Web Development",
    level: "Beginner to Advanced",
    language: "English",
    lastUpdated: "December 2024",
    bestseller: true,
    description: `This comprehensive React course will take you from beginner to advanced level. You'll learn everything you need to know to build modern, responsive web applications using React, including hooks, context, routing, and state management.`,
    whatYouWillLearn: [
      "Build modern React applications from scratch",
      "Master React Hooks and functional components",
      "Implement state management with Context API and Redux",
      "Create responsive designs with CSS and styled-components",
      "Handle forms and user input validation",
      "Work with APIs and asynchronous data",
      "Deploy applications to production",
      "Test React components and applications",
    ],
    requirements: [
      "Basic knowledge of HTML, CSS, and JavaScript",
      "A computer with internet connection",
      "No prior React experience required",
    ],
    curriculum: [
      {
        section: "Getting Started with React",
        lectures: 12,
        duration: "2h 30m",
        lessons: [
          { title: "Introduction to React", duration: "15:30", preview: true },
          { title: "Setting up Development Environment", duration: "20:45", preview: false },
          { title: "Your First React Component", duration: "18:20", preview: true },
          { title: "JSX Fundamentals", duration: "22:15", preview: false },
        ],
      },
      {
        section: "React Components and Props",
        lectures: 18,
        duration: "4h 15m",
        lessons: [
          { title: "Understanding Components", duration: "25:30", preview: false },
          { title: "Props and Data Flow", duration: "30:45", preview: false },
          { title: "Component Composition", duration: "28:20", preview: false },
        ],
      },
      {
        section: "State Management and Hooks",
        lectures: 24,
        duration: "6h 45m",
        lessons: [
          { title: "useState Hook", duration: "35:30", preview: false },
          { title: "useEffect Hook", duration: "40:45", preview: false },
          { title: "Custom Hooks", duration: "32:20", preview: false },
        ],
      },
    ],
  }

  const reviews = [
    {
      id: 1,
      user: "John Doe",
      avatar: "/placeholder.svg?height=40&width=40",
      rating: 5,
      date: "2 weeks ago",
      comment:
        "Excellent course! Sarah explains everything clearly and the projects are very practical. Highly recommended for anyone wanting to learn React.",
    },
    {
      id: 2,
      user: "Jane Smith",
      avatar: "/placeholder.svg?height=40&width=40",
      rating: 4,
      date: "1 month ago",
      comment:
        "Great content and well-structured. The instructor is knowledgeable and the pace is perfect for beginners.",
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
                <Link href="/login">Login</Link>
              </Button>
              <Button asChild>
                <Link href="/dashboard">Dashboard</Link>
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Course Header */}
      <div className="bg-gray-900 text-white py-8">
        <div className="container mx-auto px-4">
          <div className="grid lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2">
              <div className="flex items-center gap-2 mb-4">
                <Badge className="bg-orange-500">{course.category}</Badge>
                {course.bestseller && <Badge className="bg-yellow-500 text-black">Bestseller</Badge>}
              </div>

              <h1 className="text-4xl font-bold mb-4">{course.title}</h1>
              <p className="text-xl text-gray-300 mb-6">{course.subtitle}</p>

              <div className="flex items-center gap-6 mb-6">
                <div className="flex items-center">
                  <Star className="w-5 h-5 fill-yellow-400 text-yellow-400 mr-1" />
                  <span className="font-semibold mr-2">{course.rating}</span>
                  <span className="text-gray-300">({course.reviews} reviews)</span>
                </div>
                <div className="flex items-center text-gray-300">
                  <Users className="w-5 h-5 mr-1" />
                  {course.students.toLocaleString()} students
                </div>
              </div>

              <div className="flex items-center gap-4 text-gray-300">
                <span>Created by {course.instructor.name}</span>
                <span>•</span>
                <span>Last updated {course.lastUpdated}</span>
                <span>•</span>
                <div className="flex items-center">
                  <Globe className="w-4 h-4 mr-1" />
                  {course.language}
                </div>
              </div>
            </div>

            {/* Course Preview Card */}
            <div className="lg:col-span-1">
              <Card className="sticky top-24">
                <div className="relative">
                  <Image
                    src={course.image || "/placeholder.svg"}
                    alt={course.title}
                    width={600}
                    height={400}
                    className="w-full h-48 object-cover rounded-t-lg"
                  />
                  <div className="absolute inset-0 bg-black/20 flex items-center justify-center">
                    <Button size="lg" className="bg-white text-black hover:bg-gray-100">
                      <Play className="mr-2 h-5 w-5" />
                      Preview Course
                    </Button>
                  </div>
                </div>

                <CardContent className="p-6">
                  <div className="text-center mb-6">
                    <div className="text-3xl font-bold mb-2">${course.price}</div>
                    <div className="text-lg text-muted-foreground line-through">${course.originalPrice}</div>
                    <div className="text-sm text-green-600 font-medium">55% off • Limited time</div>
                  </div>

                  <div className="space-y-3 mb-6">
                    <Button className="w-full" size="lg">
                      Enroll Now
                    </Button>
                    <Button variant="outline" className="w-full">
                      Add to Cart
                    </Button>
                  </div>

                  <div className="text-center text-sm text-muted-foreground mb-4">30-Day Money-Back Guarantee</div>

                  <div className="space-y-3 text-sm">
                    <div className="flex items-center">
                      <Clock className="w-4 h-4 mr-2" />
                      {course.duration} on-demand video
                    </div>
                    <div className="flex items-center">
                      <Download className="w-4 h-4 mr-2" />
                      Downloadable resources
                    </div>
                    <div className="flex items-center">
                      <Smartphone className="w-4 h-4 mr-2" />
                      Access on mobile and TV
                    </div>
                    <div className="flex items-center">
                      <Infinity className="w-4 h-4 mr-2" />
                      Full lifetime access
                    </div>
                    <div className="flex items-center">
                      <Award className="w-4 h-4 mr-2" />
                      Certificate of completion
                    </div>
                  </div>

                  <div className="flex justify-center space-x-4 mt-6 pt-6 border-t">
                    <Button variant="ghost" size="sm">
                      <Heart className="w-4 h-4 mr-2" />
                      Wishlist
                    </Button>
                    <Button variant="ghost" size="sm">
                      <Share2 className="w-4 h-4 mr-2" />
                      Share
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </div>

      {/* Course Content */}
      <div className="container mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <Tabs defaultValue="overview" className="w-full">
              <TabsList className="grid w-full grid-cols-4">
                <TabsTrigger value="overview">Overview</TabsTrigger>
                <TabsTrigger value="curriculum">Curriculum</TabsTrigger>
                <TabsTrigger value="instructor">Instructor</TabsTrigger>
                <TabsTrigger value="reviews">Reviews</TabsTrigger>
              </TabsList>

              <TabsContent value="overview" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle>What you'll learn</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid md:grid-cols-2 gap-3">
                      {course.whatYouWillLearn.map((item, index) => (
                        <div key={index} className="flex items-start">
                          <CheckCircle className="w-5 h-5 text-green-500 mr-3 mt-0.5 flex-shrink-0" />
                          <span className="text-sm">{item}</span>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>Course Description</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-muted-foreground leading-relaxed">{course.description}</p>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>Requirements</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2">
                      {course.requirements.map((req, index) => (
                        <li key={index} className="flex items-start">
                          <span className="w-2 h-2 bg-gray-400 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                          <span className="text-sm text-muted-foreground">{req}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="curriculum">
                <Card>
                  <CardHeader>
                    <CardTitle>Course Curriculum</CardTitle>
                    <CardDescription>
                      {course.lectures} lectures • {course.duration} total length
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {course.curriculum.map((section, index) => (
                        <div key={index} className="border rounded-lg">
                          <div className="p-4 bg-gray-50 border-b">
                            <div className="flex justify-between items-center">
                              <h3 className="font-semibold">{section.section}</h3>
                              <div className="text-sm text-muted-foreground">
                                {section.lectures} lectures • {section.duration}
                              </div>
                            </div>
                          </div>
                          <div className="divide-y">
                            {section.lessons.map((lesson, lessonIndex) => (
                              <div key={lessonIndex} className="p-4 flex items-center justify-between hover:bg-gray-50">
                                <div className="flex items-center">
                                  <Play className="w-4 h-4 mr-3 text-muted-foreground" />
                                  <span className="text-sm">{lesson.title}</span>
                                  {lesson.preview && (
                                    <Badge variant="outline" className="ml-2 text-xs">
                                      Preview
                                    </Badge>
                                  )}
                                </div>
                                <span className="text-sm text-muted-foreground">{lesson.duration}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="instructor">
                <Card>
                  <CardHeader>
                    <CardTitle>About the Instructor</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="flex items-start space-x-4">
                      <Avatar className="w-20 h-20">
                        <AvatarImage src={course.instructor.avatar || "/placeholder.svg"} />
                        <AvatarFallback>SJ</AvatarFallback>
                      </Avatar>
                      <div className="flex-1">
                        <h3 className="text-xl font-semibold mb-1">{course.instructor.name}</h3>
                        <p className="text-muted-foreground mb-4">{course.instructor.title}</p>

                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                          <div className="text-center">
                            <div className="flex items-center justify-center mb-1">
                              <Star className="w-4 h-4 fill-yellow-400 text-yellow-400 mr-1" />
                              <span className="font-semibold">{course.instructor.rating}</span>
                            </div>
                            <div className="text-xs text-muted-foreground">Rating</div>
                          </div>
                          <div className="text-center">
                            <div className="font-semibold mb-1">{course.instructor.students.toLocaleString()}</div>
                            <div className="text-xs text-muted-foreground">Students</div>
                          </div>
                          <div className="text-center">
                            <div className="font-semibold mb-1">{course.instructor.courses}</div>
                            <div className="text-xs text-muted-foreground">Courses</div>
                          </div>
                        </div>

                        <p className="text-sm text-muted-foreground">
                          Sarah is a senior full-stack developer with over 8 years of experience building web
                          applications. She has worked with companies like Google and Microsoft, and is passionate about
                          teaching modern web development technologies.
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="reviews">
                <Card>
                  <CardHeader>
                    <CardTitle>Student Reviews</CardTitle>
                    <CardDescription>{course.reviews} reviews for this course</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-6">
                      {reviews.map((review) => (
                        <div key={review.id} className="border-b pb-6 last:border-b-0">
                          <div className="flex items-start space-x-4">
                            <Avatar>
                              <AvatarImage src={review.avatar || "/placeholder.svg"} />
                              <AvatarFallback>
                                {review.user
                                  .split(" ")
                                  .map((n) => n[0])
                                  .join("")}
                              </AvatarFallback>
                            </Avatar>
                            <div className="flex-1">
                              <div className="flex items-center justify-between mb-2">
                                <h4 className="font-semibold">{review.user}</h4>
                                <span className="text-sm text-muted-foreground">{review.date}</span>
                              </div>
                              <div className="flex items-center mb-2">
                                {[...Array(5)].map((_, i) => (
                                  <Star
                                    key={i}
                                    className={`w-4 h-4 ${
                                      i < review.rating ? "fill-yellow-400 text-yellow-400" : "text-gray-300"
                                    }`}
                                  />
                                ))}
                              </div>
                              <p className="text-sm text-muted-foreground">{review.comment}</p>
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

          {/* Sidebar - Related Courses */}
          <div className="lg:col-span-1">
            <Card>
              <CardHeader>
                <CardTitle>Related Courses</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {[1, 2, 3].map((i) => (
                    <div key={i} className="flex space-x-3">
                      <Image
                        src="/placeholder.svg?height=60&width=80"
                        alt="Course thumbnail"
                        width={80}
                        height={60}
                        className="rounded object-cover"
                      />
                      <div className="flex-1">
                        <h4 className="text-sm font-medium line-clamp-2 mb-1">
                          Advanced React Patterns and Best Practices
                        </h4>
                        <p className="text-xs text-muted-foreground mb-1">by John Smith</p>
                        <div className="flex items-center">
                          <Star className="w-3 h-3 fill-yellow-400 text-yellow-400 mr-1" />
                          <span className="text-xs">4.7</span>
                          <span className="text-xs text-muted-foreground ml-2">$79.99</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
