import django_filters
from .models import Course, Category

class CourseFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    difficulty_level = django_filters.ChoiceFilter(choices=Course.DIFFICULTY_CHOICES)
    is_free = django_filters.BooleanFilter()
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    rating_min = django_filters.NumberFilter(method='filter_by_rating')
    
    class Meta:
        model = Course
        fields = ['category', 'difficulty_level', 'is_free', 'language', 'is_bestseller']
    
    def filter_by_rating(self, queryset, name, value):
        # This would require a custom annotation for average rating
        return queryset
