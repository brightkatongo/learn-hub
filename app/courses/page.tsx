"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Star, Users, Clock, Search, Filter, Grid, List } from "lucide-react"
import Link from "next/link"
import Image from "next/image"

export default function CoursesPage() {
  const [viewMode, setViewMode] = useState<"grid" | "list">("grid")
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedCategory, setSelectedCategory] = useState("all")
  const [selectedLevel, setSelectedLevel] = useState("all")
  const [priceFilter, setPriceFilter] = useState("all")
  const [showFilters, setShowFilters] = useState(false)

  const courses = [
    {
      id: 1,
      title: "Complete React Developer Course",
      instructor: "Sarah Johnson",
      rating: 4.8,
      reviews: 2543,
      students: 12543,
      duration: "42 hours",
      price: 89.99,
      originalPrice: 199.99,
      image: "/placeholder.svg?height=200&width=300",
      category: "Web Development",
      level: "Beginner to Advanced",
      bestseller: true,
      description: "Learn React from scratch and build amazing web applications",
    },
    {
      id: 2,
      title: "Machine Learning Masterclass",
      instructor: "Dr. Michael Chen",
      rating: 4.9,
      reviews: 1876,
      students: 8932,
      duration: "38 hours",
      price: 94.99,
      originalPrice: 179.99,
      image: "/placeholder.svg?height=200&width=300",
      category: "Data Science",
      level: "Intermediate",
      bestseller: false,
      description: "Master machine learning algorithms and build intelligent systems",
    },
    {
      id: 3,
      title: "UI/UX Design Fundamentals",
      instructor: "Emma Rodriguez",
      rating: 4.7,
      reviews: 3421,
      students: 15678,
      duration: "28 hours",
      price: 69.99,
      originalPrice: 149.99,
      image: "/placeholder.svg?height=200&width=300",
      category: "Design",
      level: "Beginner",
      bestseller: true,
      description: "Create beautiful and user-friendly interfaces",
    },
    {
      id: 4,
      title: "Python for Data Science",
      instructor: "Alex Kumar",
      rating: 4.6,
      reviews: 1987,
      students: 9876,
      duration: "35 hours",
      price: 79.99,
      originalPrice: 159.99,
      image: "/placeholder.svg?height=200&width=300",
      category: "Data Science",
      level: "Beginner to Intermediate",
      bestseller: false,
      description: "Learn Python programming for data analysis and visualization",
    },
    {
      id: 5,
      title: "Digital Marketing Strategy",
      instructor: "Lisa Thompson",
      rating: 4.5,
      reviews: 2156,
      students: 11234,
      duration: "25 hours",
      price: 59.99,
      originalPrice: 129.99,
      image: "/placeholder.svg?height=200&width=300",
      category: "Marketing",
      level: "Beginner",
      bestseller: false,
      description: "Master digital marketing techniques and grow your business",
    },
    {
      id: 6,
      title: "Advanced JavaScript Concepts",
      instructor: "David Wilson",
      rating: 4.8,
      reviews: 1654,
      students: 7890,
      duration: "32 hours",
      price: 84.99,
      originalPrice: 169.99,
      image: "/placeholder.svg?height=200&width=300",
      category: "Web Development",
      level: "Advanced",
      bestseller: false,
      description: "Deep dive into advanced JavaScript concepts and patterns",
    },
  ]

  const categories = ["Web Development", "Data Science", "Design", "Marketing", "Business", "Photography"]

  const levels = ["Beginner", "Intermediate", "Advanced", "All Levels"]

  const filteredCourses = courses.filter((course) => {
    const matchesSearch =
      course.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      course.instructor.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesCategory = selectedCategory === "all" || course.category === selectedCategory
    const matchesLevel = selectedLevel === "all" || course.level.includes(selectedLevel)
    const matchesPrice =
      priceFilter === "all" ||
      (priceFilter === "free" && course.price === 0) ||
      (priceFilter === "paid" && course.price > 0) ||
      (priceFilter === "under50" && course.price < 50) ||
      (priceFilter === "under100" && course.price < 100)

    return matchesSearch && matchesCategory && matchesLevel && matchesPrice
  })

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
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-4">All Courses</h1>
          <p className="text-xl text-muted-foreground">
            Discover our comprehensive collection of courses designed to help you learn new skills
          </p>
        </div>

        {/* Search and Filters */}
        <div className="mb-8 space-y-4">
          <div className="flex flex-col lg:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
              <Input
                placeholder="Search courses, instructors..."
                className="pl-10"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>

            <div className="flex gap-2">
              <Button variant="outline" onClick={() => setShowFilters(!showFilters)}>
                <Filter className="mr-2 h-4 w-4" />
                Filters
              </Button>

              <div className="flex border rounded-md">
                <Button
                  variant={viewMode === "grid" ? "default" : "ghost"}
                  size="sm"
                  onClick={() => setViewMode("grid")}
                  className="rounded-r-none"
                >
                  <Grid className="h-4 w-4" />
                </Button>
                <Button
                  variant={viewMode === "list" ? "default" : "ghost"}
                  size="sm"
                  onClick={() => setViewMode("list")}
                  className="rounded-l-none"
                >
                  <List className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>

          {/* Filters Panel */}
          {showFilters && (
            <Card>
              <CardContent className="p-6">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                  <div>
                    <label className="text-sm font-medium mb-2 block">Category</label>
                    <Select value={selectedCategory} onValueChange={setSelectedCategory}>
                      <SelectTrigger>
                        <SelectValue placeholder="All Categories" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="all">All Categories</SelectItem>
                        {categories.map((category) => (
                          <SelectItem key={category} value={category.toLowerCase()}>
                            {category}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <label className="text-sm font-medium mb-2 block">Level</label>
                    <Select value={selectedLevel} onValueChange={setSelectedLevel}>
                      <SelectTrigger>
                        <SelectValue placeholder="All Levels" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="all">All Levels</SelectItem>
                        {levels.map((level) => (
                          <SelectItem key={level} value={level.toLowerCase()}>
                            {level}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <label className="text-sm font-medium mb-2 block">Price</label>
                    <Select value={priceFilter} onValueChange={setPriceFilter}>
                      <SelectTrigger>
                        <SelectValue placeholder="All Prices" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="all">All Prices</SelectItem>
                        <SelectItem value="free">Free</SelectItem>
                        <SelectItem value="paid">Paid</SelectItem>
                        <SelectItem value="under50">Under $50</SelectItem>
                        <SelectItem value="under100">Under $100</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="flex items-end">
                    <Button
                      variant="outline"
                      onClick={() => {
                        setSelectedCategory("all")
                        setSelectedLevel("all")
                        setPriceFilter("all")
                        setSearchQuery("")
                      }}
                      className="w-full"
                    >
                      Clear Filters
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Results Count */}
        <div className="mb-6">
          <p className="text-muted-foreground">
            Showing {filteredCourses.length} of {courses.length} courses
          </p>
        </div>

        {/* Courses Grid/List */}
        <div className={viewMode === "grid" ? "grid md:grid-cols-2 lg:grid-cols-3 gap-6" : "space-y-6"}>
          {filteredCourses.map((course) => (
            <Card
              key={course.id}
              className={`overflow-hidden hover:shadow-lg transition-shadow ${viewMode === "list" ? "flex" : ""}`}
            >
              <div className={viewMode === "list" ? "w-64 flex-shrink-0" : "relative"}>
                <Image
                  src={course.image || "/placeholder.svg"}
                  alt={course.title}
                  width={300}
                  height={200}
                  className={`object-cover ${viewMode === "list" ? "w-full h-full" : "w-full h-48"}`}
                />
                <div className="absolute top-2 left-2 flex gap-2">
                  <Badge className="bg-primary">{course.category}</Badge>
                  {course.bestseller && <Badge className="bg-yellow-500 text-black">Bestseller</Badge>}
                </div>
              </div>

              <div className="flex-1">
                <CardHeader>
                  <CardTitle className="line-clamp-2">
                    <Link href={`/courses/${course.id}`} className="hover:text-primary">
                      {course.title}
                    </Link>
                  </CardTitle>
                  <CardDescription>by {course.instructor}</CardDescription>
                  {viewMode === "list" && (
                    <p className="text-sm text-muted-foreground line-clamp-2">{course.description}</p>
                  )}
                </CardHeader>

                <CardContent>
                  <div className="flex items-center gap-4 text-sm text-muted-foreground mb-4">
                    <div className="flex items-center">
                      <Star className="w-4 h-4 fill-yellow-400 text-yellow-400 mr-1" />
                      {course.rating}
                      <span className="ml-1">({course.reviews})</span>
                    </div>
                    <div className="flex items-center">
                      <Users className="w-4 h-4 mr-1" />
                      {course.students.toLocaleString()}
                    </div>
                    <div className="flex items-center">
                      <Clock className="w-4 h-4 mr-1" />
                      {course.duration}
                    </div>
                  </div>

                  <div className="flex items-center justify-between">
                    <div>
                      <span className="text-2xl font-bold">${course.price}</span>
                      <span className="text-sm text-muted-foreground line-through ml-2">${course.originalPrice}</span>
                    </div>
                    <Button size="sm" asChild>
                      <Link href={`/courses/${course.id}`}>View Course</Link>
                    </Button>
                  </div>
                </CardContent>
              </div>
            </Card>
          ))}
        </div>

        {filteredCourses.length === 0 && (
          <div className="text-center py-12">
            <h3 className="text-lg font-semibold mb-2">No courses found</h3>
            <p className="text-muted-foreground mb-4">Try adjusting your search criteria or filters</p>
            <Button
              onClick={() => {
                setSelectedCategory("all")
                setSelectedLevel("all")
                setPriceFilter("all")
                setSearchQuery("")
              }}
            >
              Clear All Filters
            </Button>
          </div>
        )}
      </div>
    </div>
  )
}
