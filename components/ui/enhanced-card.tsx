"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Star, Users, Clock, Play, BookOpen, Award } from "lucide-react"
import { formatPrice } from "@/lib/currency"
import Image from "next/image"
import Link from "next/link"

interface EnhancedCardProps {
  course: {
    id: number
    title: string
    instructor: string
    rating: number
    reviews: number
    students: number
    duration: string
    price: number
    originalPrice?: number
    image: string
    category: string
    level: string
    bestseller?: boolean
    description: string
    lessons?: number
    certificate?: boolean
  }
  currency: string
  viewMode?: "grid" | "list"
  onEnroll?: (courseId: number) => void
}

export function EnhancedCard({ course, currency, viewMode = "grid", onEnroll }: EnhancedCardProps) {
  const isListView = viewMode === "list"

  return (
    <Card
      className={`group overflow-hidden hover:shadow-xl transition-all duration-300 border-0 shadow-md hover:shadow-2xl hover:-translate-y-1 ${isListView ? "flex" : ""}`}
    >
      <div className={`relative ${isListView ? "w-80 flex-shrink-0" : ""}`}>
        <div className={`relative overflow-hidden ${isListView ? "h-full" : "h-48"}`}>
          <Image
            src={course.image || "/placeholder.svg"}
            alt={course.title}
            fill
            className="object-cover transition-transform duration-300 group-hover:scale-105"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />

          {/* Badges */}
          <div className="absolute top-3 left-3 flex gap-2">
            <Badge className="bg-primary/90 backdrop-blur-sm text-white border-0">{course.category}</Badge>
            {course.bestseller && (
              <Badge className="bg-yellow-500/90 backdrop-blur-sm text-black border-0">⭐ Bestseller</Badge>
            )}
          </div>

          {/* Play button overlay */}
          <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
            <div className="bg-white/20 backdrop-blur-sm rounded-full p-4">
              <Play className="h-8 w-8 text-white fill-white" />
            </div>
          </div>
        </div>
      </div>

      <div className="flex-1 flex flex-col">
        <CardHeader className="pb-3">
          <div className="flex items-start justify-between gap-2">
            <div className="flex-1">
              <CardTitle className="line-clamp-2 text-lg font-bold group-hover:text-primary transition-colors">
                <Link href={`/courses/${course.id}`}>{course.title}</Link>
              </CardTitle>
              <CardDescription className="mt-1 font-medium text-primary/70">by {course.instructor}</CardDescription>
            </div>

            {course.certificate && <Award className="h-5 w-5 text-yellow-500 flex-shrink-0" />}
          </div>

          {isListView && <p className="text-sm text-muted-foreground line-clamp-2 mt-2">{course.description}</p>}
        </CardHeader>

        <CardContent className="flex-1 flex flex-col justify-between">
          {/* Stats */}
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div className="flex items-center gap-2 text-sm">
              <div className="flex items-center gap-1">
                <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                <span className="font-semibold">{course.rating}</span>
              </div>
              <span className="text-muted-foreground">({course.reviews})</span>
            </div>

            <div className="flex items-center gap-1 text-sm text-muted-foreground">
              <Users className="h-4 w-4" />
              <span>{course.students.toLocaleString()}</span>
            </div>

            <div className="flex items-center gap-1 text-sm text-muted-foreground">
              <Clock className="h-4 w-4" />
              <span>{course.duration}</span>
            </div>

            {course.lessons && (
              <div className="flex items-center gap-1 text-sm text-muted-foreground">
                <BookOpen className="h-4 w-4" />
                <span>{course.lessons} lessons</span>
              </div>
            )}
          </div>

          {/* Level Badge */}
          <div className="mb-4">
            <Badge variant="secondary" className="text-xs">
              {course.level}
            </Badge>
          </div>

          {/* Price and Action */}
          <div className="flex items-center justify-between">
            <div className="flex items-baseline gap-2">
              <span className="text-2xl font-bold text-primary">{formatPrice(course.price, currency)}</span>
              {course.originalPrice && (
                <span className="text-sm text-muted-foreground line-through">
                  {formatPrice(course.originalPrice, currency)}
                </span>
              )}
            </div>

            <Button
              size="sm"
              className="bg-primary hover:bg-primary/90 text-white shadow-lg hover:shadow-xl transition-all duration-200"
              onClick={() => onEnroll?.(course.id)}
            >
              Enroll Now
            </Button>
          </div>
        </CardContent>
      </div>
    </Card>
  )
}
