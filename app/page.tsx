"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { EnhancedCard } from "@/components/ui/enhanced-card"
import { CurrencySelector } from "@/components/ui/currency-selector"
import { PaymentModal } from "@/components/ui/payment-modal"
import { detectUserCurrency } from "@/lib/currency"
import { useAuth } from "@/components/auth-provider"
import {
  Search,
  BookOpen,
  Users,
  Award,
  TrendingUp,
  ChevronRight,
  Globe,
  Smartphone,
  Clock,
  CheckCircle,
} from "lucide-react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { useToast } from "@/hooks/use-toast"

export default function HomePage() {
  const [currency, setCurrency] = useState("USD")
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedCourse, setSelectedCourse] = useState<any>(null)
  const [showPaymentModal, setShowPaymentModal] = useState(false)
  const { user } = useAuth()
  const router = useRouter()
  const { toast } = useToast()

  useEffect(() => {
    setCurrency(detectUserCurrency())
  }, [])

  const featuredCourses = [
    {
      id: 1,
      title: "Complete Web Development Bootcamp",
      instructor: "Sarah Johnson",
      rating: 4.9,
      reviews: 3245,
      students: 15678,
      duration: "52 hours",
      price: 89.99,
      originalPrice: 199.99,
      image: "/placeholder.svg?height=200&width=300",
      category: "Web Development",
      level: "Beginner to Advanced",
      bestseller: true,
      description: "Learn HTML, CSS, JavaScript, React, Node.js and build real-world projects",
      lessons: 156,
      certificate: true,
    },
    {
      id: 2,
      title: "Digital Marketing for African Businesses",
      instructor: "Kwame Asante",
      rating: 4.8,
      reviews: 1876,
      students: 8932,
      duration: "28 hours",
      price: 59.99,
      originalPrice: 129.99,
      image: "/placeholder.svg?height=200&width=300",
      category: "Marketing",
      level: "Beginner",
      bestseller: true,
      description: "Master digital marketing strategies tailored for African markets",
      lessons: 89,
      certificate: true,
    },
    {
      id: 3,
      title: "Mobile App Development with React Native",
      instructor: "Amina Kone",
      rating: 4.7,
      reviews: 2156,
      students: 11234,
      duration: "45 hours",
      price: 79.99,
      originalPrice: 159.99,
      image: "/placeholder.svg?height=200&width=300",
      category: "Mobile Development",
      level: "Intermediate",
      bestseller: false,
      description: "Build cross-platform mobile apps for iOS and Android",
      lessons: 124,
      certificate: true,
    },
  ]

  const stats = [
    { icon: BookOpen, label: "Courses", value: "500+", color: "text-blue-600" },
    { icon: Users, label: "Students", value: "50K+", color: "text-green-600" },
    { icon: Award, label: "Certificates", value: "25K+", color: "text-yellow-600" },
    { icon: TrendingUp, label: "Success Rate", value: "95%", color: "text-purple-600" },
  ]

  const features = [
    {
      icon: Globe,
      title: "Learn Anywhere",
      description: "Access courses from anywhere in Africa and beyond with offline support",
    },
    {
      icon: Smartphone,
      title: "Mobile-First",
      description: "Optimized for mobile learning with data-efficient streaming",
    },
    {
      icon: Clock,
      title: "Flexible Schedule",
      description: "Learn at your own pace with lifetime access to course materials",
    },
    {
      icon: CheckCircle,
      title: "Certified Learning",
      description: "Earn industry-recognized certificates upon course completion",
    },
  ]

  const handleEnroll = (course: any) => {
    if (!user) {
      toast({
        title: "Please sign in",
        description: "You need to sign in to enroll in courses",
      })
      router.push("/login")
      return
    }

    setSelectedCourse(course)
    setShowPaymentModal(true)
  }

  const handlePaymentSuccess = () => {
    toast({
      title: "Enrollment successful!",
      description: `You've successfully enrolled in ${selectedCourse?.title}`,
    })
    router.push("/dashboard")
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Link
              href="/"
              className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent"
            >
              LearnHub
            </Link>

            <div className="hidden md:flex items-center space-x-8">
              <Link href="/courses" className="text-gray-700 hover:text-primary transition-colors">
                Courses
              </Link>
              <Link href="/about" className="text-gray-700 hover:text-primary transition-colors">
                About
              </Link>
              <Link href="/contact" className="text-gray-700 hover:text-primary transition-colors">
                Contact
              </Link>
            </div>

            <div className="flex items-center space-x-4">
              <CurrencySelector selectedCurrency={currency} onCurrencyChange={setCurrency} />

              {user ? (
                <Button asChild>
                  <Link href="/dashboard">Dashboard</Link>
                </Button>
              ) : (
                <div className="flex items-center space-x-2">
                  <Button variant="outline" asChild>
                    <Link href="/login">Sign In</Link>
                  </Button>
                  <Button asChild>
                    <Link href="/signup">Get Started</Link>
                  </Button>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto text-center">
          <div className="max-w-4xl mx-auto">
            <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-blue-600 via-purple-600 to-teal-600 bg-clip-text text-transparent">
              Learn Skills That Matter
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 mb-8 leading-relaxed">
              Join Africa's premier online learning platform. Master in-demand skills from expert instructors and
              advance your career with courses designed for the modern world.
            </p>

            {/* Search Bar */}
            <div className="max-w-2xl mx-auto mb-8">
              <div className="relative">
                <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <Input
                  placeholder="What do you want to learn today?"
                  className="pl-12 pr-4 py-4 text-lg border-2 border-gray-200 focus:border-primary rounded-full"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
                <Button
                  className="absolute right-2 top-1/2 transform -translate-y-1/2 rounded-full px-6"
                  onClick={() => router.push(`/courses?search=${searchQuery}`)}
                >
                  Search
                </Button>
              </div>
            </div>

            <div className="flex flex-wrap justify-center gap-4 mb-12">
              <Badge variant="secondary" className="px-4 py-2 text-sm">
                🌍 Available in Local Languages
              </Badge>
              <Badge variant="secondary" className="px-4 py-2 text-sm">
                📱 Mobile Money Payments
              </Badge>
              <Badge variant="secondary" className="px-4 py-2 text-sm">
                🎓 Industry Certificates
              </Badge>
            </div>

            <Button
              size="lg"
              className="text-lg px-8 py-4 rounded-full shadow-lg hover:shadow-xl transition-all duration-200"
              asChild
            >
              <Link href="/courses">
                Explore Courses
                <ChevronRight className="ml-2 h-5 w-5" />
              </Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className={`inline-flex items-center justify-center w-16 h-16 rounded-full bg-gray-100 mb-4`}>
                  <stat.icon className={`h-8 w-8 ${stat.color}`} />
                </div>
                <div className="text-3xl font-bold text-gray-900 mb-2">{stat.value}</div>
                <div className="text-gray-600">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Courses */}
      <section className="py-20 px-4">
        <div className="container mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4">Featured Courses</h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Discover our most popular courses, carefully selected to help you build the skills employers are looking
              for
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
            {featuredCourses.map((course) => (
              <EnhancedCard key={course.id} course={course} currency={currency} onEnroll={handleEnroll} />
            ))}
          </div>

          <div className="text-center">
            <Button size="lg" variant="outline" asChild>
              <Link href="/courses">
                View All Courses
                <ChevronRight className="ml-2 h-5 w-5" />
              </Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Why Choose LearnHub?</h2>
            <p className="text-xl opacity-90 max-w-2xl mx-auto">
              We're built for African learners, with features that work in your environment
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="text-center">
                <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-white/20 backdrop-blur-sm mb-6">
                  <feature.icon className="h-8 w-8" />
                </div>
                <h3 className="text-xl font-semibold mb-3">{feature.title}</h3>
                <p className="opacity-90">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 bg-gray-50">
        <div className="container mx-auto text-center">
          <div className="max-w-3xl mx-auto">
            <h2 className="text-4xl font-bold mb-6">Ready to Start Learning?</h2>
            <p className="text-xl text-gray-600 mb-8">
              Join thousands of students who are already building their future with LearnHub
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" className="text-lg px-8 py-4" asChild>
                <Link href="/signup">Start Learning Today</Link>
              </Button>
              <Button size="lg" variant="outline" className="text-lg px-8 py-4" asChild>
                <Link href="/courses">Browse Courses</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Payment Modal */}
      {selectedCourse && (
        <PaymentModal
          isOpen={showPaymentModal}
          onClose={() => setShowPaymentModal(false)}
          course={selectedCourse}
          currency={currency}
          onPaymentSuccess={handlePaymentSuccess}
        />
      )}
    </div>
  )
}
