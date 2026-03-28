"""
Django management command to populate sample wellness content.
Run with: python manage.py populate_wellness_content
"""
from django.core.management.base import BaseCommand
from student.models import MeditationGuide, BreathingExercise, MotivationalContent


class Command(BaseCommand):
    help = 'Populate database with sample wellness content'

    def handle(self, *args, **options):
        # Sample Meditation Guides
        meditations = [
            {
                'title': '5-Minute Morning Meditation',
                'description': 'Start your day with clarity and calm. A gentle 5-minute meditation to set positive intentions.',
                'video_url': 'https://www.youtube.com/embed/z6X3V8AUqZE',
                'duration': 5,
                'difficulty': 'Beginner',
            },
            {
                'title': 'Mindfulness Meditation for Sleep',
                'description': 'Wind down in the evening with this soothing meditation designed to help you relax and sleep better.',
                'video_url': 'https://www.youtube.com/embed/W3xFqcJlYHo',
                'duration': 15,
                'difficulty': 'Beginner',
            },
            {
                'title': 'Body Scan Relaxation',
                'description': 'Release tension from your body while improving awareness and relaxation through guided scanning.',
                'video_url': 'https://www.youtube.com/embed/H_uc-uQ3Nkc',
                'duration': 10,
                'difficulty': 'Beginner',
            },
        ]

        count = 0
        for med in meditations:
            try:
                MeditationGuide.objects.get(title=med['title'])
            except MeditationGuide.DoesNotExist:
                MeditationGuide(
                    title=med['title'],
                    description=med['description'],
                    video_url=med['video_url'],
                    duration=med['duration'],
                    difficulty=med['difficulty'],
                ).save()
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Created {count} new meditation guides'))

        # Sample Breathing Exercises
        exercises = [
            {
                'title': '4-7-8 Breathing Technique',
                'description': 'A calming breathing pattern that helps reduce anxiety and promote relaxation.',
                'instructions': 'Step 1: Exhale completely through your mouth.\nStep 2: Close your mouth, inhale through nose for count of 4.\nStep 3: Hold your breath for count of 7.\nStep 4: Exhale through mouth for count of 8.\nRepeat 4 more times.',
                'video_url': 'https://www.youtube.com/embed/YJ2jUAm5AkQ',
                'duration': 5,
            },
            {
                'title': 'Box Breathing',
                'description': 'Also known as square breathing, this technique helps calm the nervous system.',
                'instructions': 'Step 1: Breathe in through your nose for 4 counts.\nStep 2: Hold for 4 counts.\nStep 3: Exhale through your mouth for 4 counts.\nStep 4: Hold for 4 counts.\nRepeat 5-10 times.',
                'video_url': 'https://www.youtube.com/embed/W3xFqcJlYHo',
                'duration': 5,
            },
            {
                'title': 'Diaphragmatic Breathing',
                'description': 'Deep belly breathing that activates your parasympathetic nervous system.',
                'instructions': 'Step 1: Sit or lie in a comfortable position.\nStep 2: Place one hand on your chest and one on your belly.\nStep 3: Breathe in slowly through your nose, letting your belly expand (not your chest).\nStep 4: Hold for 2-3 seconds.\nStep 5: Exhale slowly through your mouth.\nDo this for 5-10 minutes daily.',
                'video_url': 'https://www.youtube.com/embed/z6X3V8AUqZE',
                'duration': 10,
            },
        ]

        count = 0
        for ex in exercises:
            try:
                BreathingExercise.objects.get(title=ex['title'])
            except BreathingExercise.DoesNotExist:
                BreathingExercise(
                    title=ex['title'],
                    description=ex['description'],
                    instructions=ex['instructions'],
                    video_url=ex['video_url'],
                    duration=ex['duration'],
                ).save()
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Created {count} new breathing exercises'))

        # Sample Motivational Content
        motivations = [
            {
                'title': 'You Are Stronger Than You Think',
                'content': 'Every challenge you face is an opportunity to grow. The difficulties you face build your character and resilience. Remember: what feels impossible today will feel like nothing once you overcome it. You have the strength within you to handle whatever comes your way.',
                'author': 'Wellify Team',
                'category': 'Resilience',
            },
            {
                'title': 'Progress, Not Perfection',
                'content': 'Mental health is not a destination—it\'s a journey. Small steps forward are still progress. You don\'t need to be perfect; you just need to keep trying. Celebrate every small victory, every moment of self-care, and every time you choose your wellbeing. That\'s what matters.',
                'author': 'Wellify Team',
                'category': 'Recovery',
            },
            {
                'title': 'You Are Not Alone',
                'content': 'Millions of people struggle with anxiety, depression, and stress. You are not broken, and you are not alone. Reaching out for help is a sign of strength, not weakness. Your feelings are valid, and your experience matters. There are people ready to support you.',
                'author': 'Wellify Team',
                'category': 'Support',
            },
            {
                'title': 'Self-Care Is Not Selfish',
                'content': 'Taking care of yourself is essential, not optional. Just as an airplane requires oxygen masks on passengers before takeoff, you must take care of yourself first. When you invest in your wellbeing, you\'re better able to show up for others. Self-care is an investment in your ability to live fully.',
                'author': 'Wellify Team',
                'category': 'Inspiration',
            },
            {
                'title': 'Your Story Is Not Over',
                'content': 'No matter what you\'re going through right now, remember that this is not the end of your story—it\'s just a chapter. Every ending leads to a new beginning. You have survived 100% of your worst days. That\'s a perfect track record. Keep going.',
                'author': 'Wellify Team',
                'category': 'Hope',
            },
        ]

        count = 0
        for mot in motivations:
            try:
                MotivationalContent.objects.get(title=mot['title'])
            except MotivationalContent.DoesNotExist:
                MotivationalContent(
                    title=mot['title'],
                    content=mot['content'],
                    author=mot['author'],
                    category=mot['category'],
                ).save()
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Created {count} new motivational content items'))

        self.stdout.write(self.style.SUCCESS('✅ Wellness content population complete!'))
