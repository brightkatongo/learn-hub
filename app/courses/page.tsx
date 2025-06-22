import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Checkbox } from "@/components/ui/checkbox"
import { Star, Users, Clock, Filter, Search, Grid, List } from "lucide-react"
import Link from "next/link"
import Image from "next/image"

export default function CoursesPage() {
  const courses = [
    {
      id: 1,
      title: "Complete React Developer Course",
      instructor: "Sarah Johnson",
      rating: 4.8,
      reviews: 2543,
      students: 12543,
      duration: "42 hours",
      lectures: 156,
      price: 89.99,
      originalPrice: 199.99,
      image: "/placeholder.svg?height=200&width=300",
      category: "Web Development",
      level: "Beginner to Advanced",
      bestseller: true,
      updated: "Updated 2024",
    },
    {
      id: 2,
      title: "Machine Learning Masterclass",
      instructor: "Dr. Michael Chen",
      rating: 4.9,
      reviews: 1832,
      students: 8932,
      duration: "38 hours",
      lectures: 124,
      price: 94.99,
      originalPrice: 179.99,
      image: "/placeholder.svg?height=200&width=300",
      category: "Data Science",
      level: "Intermediate",
      bestseller: false,
      updated: "Updated 2024",
    },
    {
      id: 3,
      title: "UI/UX Design Fundamentals",
      instructor: "Emma Rodriguez",
      rating: 4.7,
      reviews: 3421,
      students: 15678,
      duration: "28 hours",
      lectures: 89,
      price: 69.99,
      originalPrice: 149.99,
      image: "/placeholder.svg?height=200&width=300",
      category: "Design",
      level: "Beginner",
      bestseller: true,
      updated: "Updated 2024",
    },
    {
      id: 4,
      title: "Python for Data Science",
      instructor: "James Wilson",
      rating: 4.6,
      reviews: 1987,
      students: 9876,
      duration: "35 hours",
      lectures: 142,
      price: 79.99,
      originalPrice: 159.99,
      image: "/placeholder.svg?height=200&width=300",
      category: "Programming",
      level: "Beginner to Intermediate",
      bestseller: false,
      updated: "Updated 2024",
    },
  ]

  const categories = [
    "Web Development",
    "Data Science",
    "Design",
    "Programming",
    "Business",
    "Marketing",
    "Photography",
  ]

  const levels = ["Beginner", "Intermediate", "Advanced", "All Levels"]

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

      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Sidebar Filters */}
          <div className="lg:w-1/4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Filter className="mr-2 h-5 w-5" />
                  Filters
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Search */}
                <div>
                  <label className="text-sm font-medium mb-2 block">Search</label>
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
                    <Input placeholder="Search courses..." className="pl-10" />
                  </div>
                </div>

                {/* Category */}
                <div>
                  <label className="text-sm font-medium mb-2 block">Category</label>
                  <div className="space-y-2">
                    {categories.map((category) => (
                      <div key={category} className="flex items-center space-x-2">
                        <Checkbox id={category} />
                        <label htmlFor={category} className="text-sm">
                          {category}
                        </label>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Level */}
                <div>
                  <label className="text-sm font-medium mb-2 block">Level</label>
                  <div className="space-y-2">
                    {levels.map((level) => (
                      <div key={level} className="flex items-center space-x-2">
                        <Checkbox id={level} />
                        <label htmlFor={level} className="text-sm">
                          {level}
                        </label>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Price */}
                <div>
                  <label className="text-sm font-medium mb-2 block">Price</label>
                  <div className="space-y-2">
                    <div className="flex items-center space-x-2">
                      <Checkbox id="free" />
                      <label htmlFor="free" className="text-sm">
                        Free
                      </label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Checkbox id="paid" />
                      <label htmlFor="paid" className="text-sm">
                        Paid
                      </label>
                    </div>
                  </div>
                </div>

                {/* Rating */}
                <div>
                  <label className="text-sm font-medium mb-2 block">Rating</label>
                  <div className="space-y-2">
                    {[4.5, 4.0, 3.5, 3.0].map((rating) => (
                      <div key={rating} className="flex items-center space-x-2">
                        <Checkbox id={`rating-${rating}`} />
                        <label htmlFor={`rating-${rating}`} className="text-sm flex items-center">
                          <Star className="w-4 h-4 fill-yellow-400 text-yellow-400 mr-1" />
                          {rating} & up
                        </label>
                      </div>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Main Content */}
          <div className="lg:w-3/4">
            {/* Header */}
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6">
              <div>
                <h1 className="text-3xl font-bold mb-2">All Courses</h1>
                <p className="text-muted-foreground">{courses.length} courses found</p>
              </div>

              <div className="flex items-center space-x-4 mt-4 sm:mt-0">
                <Select defaultValue="popular">
                  <SelectTrigger className="w-40">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="popular">Most Popular</SelectItem>
                    <SelectItem value="newest">Newest</SelectItem>
                    <SelectItem value="rating">Highest Rated</SelectItem>
                    <SelectItem value="price-low">Price: Low to High</SelectItem>
                    <SelectItem value="price-high">Price: High to Low</SelectItem>
                  </SelectContent>
                </Select>

                <div className="flex border rounded-md">
                  <Button variant="ghost" size="sm" className="rounded-r-none">
                    <Grid className="h-4 w-4" />
                  </Button>
                  <Button variant="ghost" size="sm" className="rounded-l-none">
                    <List className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </div>

            {/* Course Grid */}
            <div className="grid md:grid-cols-2 gap-6">
              {courses.map((course) => (
                <Card key={course.id} className="overflow-hidden hover:shadow-lg transition-shadow">
                  <div className="flex">
                    <div className="relative w-48 h-32 flex-shrink-0">
                      <Image
                        src={course.image || "/placeholder.svg"}
                        alt={course.title}
                        fill
                        className="object-cover"
                      />
                      {course.bestseller && <Badge className="absolute top-2 left-2 bg-orange-500">Bestseller</Badge>}
                    </div>

                    <div className="flex-1 p-4">
                      <div className="flex justify-between items-start mb-2">
                        <Badge variant="secondary" className="text-xs">
                          {course.category}
                        </Badge>
                        <div className="text-right">
                          <div className="text-lg font-bold">${course.price}</div>
                          <div className="text-sm text-muted-foreground line-through">${course.originalPrice}</div>
                        </div>
                      </div>

                      <h3 className="font-semibold mb-1 line-clamp-2">
                        <Link href={`/courses/${course.id}`} className="hover:text-primary">
                          {course.title}
                        </Link>
                      </h3>

                      <p className="text-sm text-muted-foreground mb-2">by {course.instructor}</p>

                      <div className="flex items-center gap-4 text-xs text-muted-foreground mb-2">
                        <div className="flex items-center">
                          <Star className="w-3 h-3 fill-yellow-400 text-yellow-400 mr-1" />
                          {course.rating} ({course.reviews})
                        </div>
                        <div className="flex items-center">
                          <Users className="w-3 h-3 mr-1" />
                          {course.students.toLocaleString()}
                        </div>
                        <div className="flex items-center">
                          <Clock className="w-3 h-3 mr-1" />
                          {course.duration}
                        </div>
                      </div>

                      <div className="flex items-center justify-between">
                        <span className="text-xs text-muted-foreground">{course.updated}</span>
                        <Button size="sm" asChild>
                          <Link href={`/courses/${course.id}`}>View Course</Link>
                        </Button>
                      </div>
                    </div>
                  </div>
                </Card>
              ))}
            </div>

            {/* Pagination */}
            <div className="flex justify-center mt-8">
              <div className="flex space-x-2">
                <Button variant="outline" disabled>
                  Previous
                </Button>
                <Button variant="outline" className="bg-primary text-white">
                  1
                </Button>
                <Button variant="outline">2</Button>
                <Button variant="outline">3</Button>
                <Button variant="outline">Next</Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
