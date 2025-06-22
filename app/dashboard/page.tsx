import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { BookOpen, Clock, Award, TrendingUp, Play, Calendar, Target, Star, Download } from "lucide-react"
import Link from "next/link"
import Image from "next/image"

export default function DashboardPage() {
  const enrolledCourses = [
    {
      id: 1,
      title: "Complete React Developer Course",
      instructor: "Sarah Johnson",
      progress: 65,
      totalLessons: 156,
      completedLessons: 101,
      timeSpent: "28h 45m",
      lastAccessed: "2 hours ago",
      image: "/placeholder.svg?height=100&width=150",
      nextLesson: "React Hooks Advanced Patterns",
    },
    {
      id: 2,
      title: "Machine Learning Masterclass",
      instructor: "Dr. Michael Chen",
      progress: 30,
      totalLessons: 124,
      completedLessons: 37,
      timeSpent: "15h 20m",
      lastAccessed: "1 day ago",
      image: "/placeholder.svg?height=100&width=150",
      nextLesson: "Linear Regression Implementation",
    },
    {
      id: 3,
      title: "UI/UX Design Fundamentals",
      instructor: "Emma Rodriguez",
      progress: 85,
      totalLessons: 89,
      completedLessons: 76,
      timeSpent: "22h 10m",
      lastAccessed: "3 hours ago",
      image: "/placeholder.svg?height=100&width=150",
      nextLesson: "Prototyping with Figma",
    },
  ]

  const achievements = [
    {
      title: "First Course Completed",
      description: "Completed your first course",
      icon: "🎓",
      earned: true,
      date: "Dec 15, 2024",
    },
    {
      title: "Week Streak",
      description: "Learned for 7 consecutive days",
      icon: "🔥",
      earned: true,
      date: "Dec 20, 2024",
    },
    {
      title: "Quick Learner",
      description: "Complete 5 lessons in one day",
      icon: "⚡",
      earned: false,
      date: null,
    },
    {
      title: "Knowledge Seeker",
      description: "Enroll in 10 courses",
      icon: "📚",
      earned: false,
      date: null,
    },
  ]

  const upcomingDeadlines = [
    {
      course: "React Developer Course",
      assignment: "Build a Todo App",
      dueDate: "Dec 28, 2024",
      type: "Project",
    },
    {
      course: "Machine Learning",
      assignment: "Linear Regression Quiz",
      dueDate: "Dec 30, 2024",
      type: "Quiz",
    },
  ]

  const learningStats = {
    totalHours: 66,
    coursesCompleted: 2,
    coursesInProgress: 3,
    certificatesEarned: 2,
    currentStreak: 5,
    longestStreak: 12,
  }

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
                <Link href="/courses">Browse Courses</Link>
              </Button>
              <Avatar>
                <AvatarImage src="/placeholder.svg?height=32&width=32" />
                <AvatarFallback>JD</AvatarFallback>
              </Avatar>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Welcome back, John! 👋</h1>
          <p className="text-muted-foreground">Continue your learning journey. You're doing great!</p>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
          <Card>
            <CardContent className="p-4 text-center">
              <Clock className="w-8 h-8 mx-auto mb-2 text-blue-500" />
              <div className="text-2xl font-bold">{learningStats.totalHours}h</div>
              <div className="text-xs text-muted-foreground">Total Hours</div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4 text-center">
              <Award className="w-8 h-8 mx-auto mb-2 text-green-500" />
              <div className="text-2xl font-bold">{learningStats.coursesCompleted}</div>
              <div className="text-xs text-muted-foreground">Completed</div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4 text-center">
              <BookOpen className="w-8 h-8 mx-auto mb-2 text-purple-500" />
              <div className="text-2xl font-bold">{learningStats.coursesInProgress}</div>
              <div className="text-xs text-muted-foreground">In Progress</div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4 text-center">
              <Star className="w-8 h-8 mx-auto mb-2 text-yellow-500" />
              <div className="text-2xl font-bold">{learningStats.certificatesEarned}</div>
              <div className="text-xs text-muted-foreground">Certificates</div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4 text-center">
              <TrendingUp className="w-8 h-8 mx-auto mb-2 text-orange-500" />
              <div className="text-2xl font-bold">{learningStats.currentStreak}</div>
              <div className="text-xs text-muted-foreground">Day Streak</div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4 text-center">
              <Target className="w-8 h-8 mx-auto mb-2 text-red-500" />
              <div className="text-2xl font-bold">{learningStats.longestStreak}</div>
              <div className="text-xs text-muted-foreground">Best Streak</div>
            </CardContent>
          </Card>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2">
            <Tabs defaultValue="courses" className="w-full">
              <TabsList className="grid w-full grid-cols-3">
                <TabsTrigger value="courses">My Courses</TabsTrigger>
                <TabsTrigger value="achievements">Achievements</TabsTrigger>
                <TabsTrigger value="certificates">Certificates</TabsTrigger>
              </TabsList>

              <TabsContent value="courses" className="space-y-4">
                <div className="flex justify-between items-center">
                  <h2 className="text-xl font-semibold">Continue Learning</h2>
                  <Button variant="outline" size="sm" asChild>
                    <Link href="/courses">Browse More</Link>
                  </Button>
                </div>

                {enrolledCourses.map((course) => (
                  <Card key={course.id} className="overflow-hidden">
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
                              <p className="text-sm text-muted-foreground">by {course.instructor}</p>
                            </div>
                            <Badge variant="secondary">{course.progress}% Complete</Badge>
                          </div>

                          <Progress value={course.progress} className="mb-3" />

                          <div className="flex items-center justify-between text-sm text-muted-foreground mb-3">
                            <span>
                              {course.completedLessons} of {course.totalLessons} lessons
                            </span>
                            <span>{course.timeSpent} spent</span>
                          </div>

                          <div className="flex items-center justify-between">
                            <div>
                              <p className="text-sm font-medium">Next: {course.nextLesson}</p>
                              <p className="text-xs text-muted-foreground">Last accessed {course.lastAccessed}</p>
                            </div>
                            <Button size="sm" asChild>
                              <Link href={`/courses/${course.id}/learn`}>
                                <Play className="w-4 h-4 mr-2" />
                                Continue
                              </Link>
                            </Button>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </TabsContent>

              <TabsContent value="achievements" className="space-y-4">
                <h2 className="text-xl font-semibold">Your Achievements</h2>

                <div className="grid md:grid-cols-2 gap-4">
                  {achievements.map((achievement, index) => (
                    <Card
                      key={index}
                      className={`${achievement.earned ? "border-green-200 bg-green-50" : "border-gray-200"}`}
                    >
                      <CardContent className="p-4">
                        <div className="flex items-start space-x-3">
                          <div className={`text-2xl ${achievement.earned ? "" : "grayscale opacity-50"}`}>
                            {achievement.icon}
                          </div>
                          <div className="flex-1">
                            <h3
                              className={`font-semibold ${achievement.earned ? "text-green-800" : "text-muted-foreground"}`}
                            >
                              {achievement.title}
                            </h3>
                            <p className={`text-sm ${achievement.earned ? "text-green-600" : "text-muted-foreground"}`}>
                              {achievement.description}
                            </p>
                            {achievement.earned && achievement.date && (
                              <p className="text-xs text-green-500 mt-1">Earned on {achievement.date}</p>
                            )}
                          </div>
                          {achievement.earned && <Badge className="bg-green-500">Earned</Badge>}
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </TabsContent>

              <TabsContent value="certificates" className="space-y-4">
                <h2 className="text-xl font-semibold">Your Certificates</h2>

                <div className="grid md:grid-cols-2 gap-4">
                  <Card>
                    <CardContent className="p-4">
                      <div className="flex items-center space-x-3">
                        <Award className="w-12 h-12 text-yellow-500" />
                        <div className="flex-1">
                          <h3 className="font-semibold">UI/UX Design Fundamentals</h3>
                          <p className="text-sm text-muted-foreground">Completed on Dec 15, 2024</p>
                          <p className="text-xs text-muted-foreground">by Emma Rodriguez</p>
                        </div>
                        <Button size="sm" variant="outline">
                          <Download className="w-4 h-4 mr-2" />
                          Download
                        </Button>
                      </div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardContent className="p-4">
                      <div className="flex items-center space-x-3">
                        <Award className="w-12 h-12 text-yellow-500" />
                        <div className="flex-1">
                          <h3 className="font-semibold">JavaScript Fundamentals</h3>
                          <p className="text-sm text-muted-foreground">Completed on Nov 28, 2024</p>
                          <p className="text-xs text-muted-foreground">by Mark Thompson</p>
                        </div>
                        <Button size="sm" variant="outline">
                          <Download className="w-4 h-4 mr-2" />
                          Download
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </TabsContent>
            </Tabs>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Learning Goal */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Target className="w-5 h-5 mr-2" />
                  Weekly Goal
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between text-sm">
                    <span>5 hours this week</span>
                    <span>3.5h / 5h</span>
                  </div>
                  <Progress value={70} />
                  <p className="text-xs text-muted-foreground">You're 70% towards your weekly goal! Keep it up! 🎯</p>
                </div>
              </CardContent>
            </Card>

            {/* Upcoming Deadlines */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Calendar className="w-5 h-5 mr-2" />
                  Upcoming Deadlines
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {upcomingDeadlines.map((deadline, index) => (
                    <div
                      key={index}
                      className="flex items-start space-x-3 p-3 bg-orange-50 rounded-lg border border-orange-200"
                    >
                      <div className="w-2 h-2 bg-orange-500 rounded-full mt-2 flex-shrink-0"></div>
                      <div className="flex-1">
                        <p className="text-sm font-medium">{deadline.assignment}</p>
                        <p className="text-xs text-muted-foreground">{deadline.course}</p>
                        <div className="flex items-center justify-between mt-1">
                          <Badge variant="outline" className="text-xs">
                            {deadline.type}
                          </Badge>
                          <span className="text-xs text-orange-600 font-medium">Due {deadline.dueDate}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Recommended Courses */}
            <Card>
              <CardHeader>
                <CardTitle>Recommended for You</CardTitle>
                <CardDescription>Based on your learning history</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {[1, 2].map((i) => (
                    <div key={i} className="flex space-x-3">
                      <Image
                        src="/placeholder.svg?height=60&width=80"
                        alt="Course thumbnail"
                        width={80}
                        height={60}
                        className="rounded object-cover"
                      />
                      <div className="flex-1">
                        <h4 className="text-sm font-medium line-clamp-2 mb-1">Advanced React Patterns</h4>
                        <p className="text-xs text-muted-foreground mb-1">by Sarah Johnson</p>
                        <div className="flex items-center justify-between">
                          <div className="flex items-center">
                            <Star className="w-3 h-3 fill-yellow-400 text-yellow-400 mr-1" />
                            <span className="text-xs">4.8</span>
                          </div>
                          <Button size="sm" variant="outline" className="text-xs h-6">
                            Enroll
                          </Button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Study Streak */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">🔥 Study Streak</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-center">
                  <div className="text-3xl font-bold text-orange-500 mb-2">{learningStats.currentStreak}</div>
                  <p className="text-sm text-muted-foreground mb-3">Days in a row</p>
                  <p className="text-xs text-muted-foreground">
                    Your longest streak: {learningStats.longestStreak} days
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
