from django.contrib import admin
from .models import UserProfile, TranslationHistory

# ১. প্রোফাইল এডমিন প্যানেলে দেখার জন্য
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'image') # প্যানেলের লিস্টে যা যা দেখাবে
    search_fields = ('user__username', 'user__email') # সার্চ করার অপশন

# ২. ট্রান্সলেশন হিস্ট্রি এডমিন প্যানেলে দেখার জন্য
@admin.register(TranslationHistory)
class TranslationHistoryAdmin(admin.ModelAdmin):
    # লিস্টে যা যা কলাম হিসেবে দেখাবে
    list_display = ('user', 'source_text_short', 'target_lang', 'created_at')
    
    # ডানপাশে ফিল্টার করার অপশন (যেমন: ল্যাঙ্গুয়েজ বা তারিখ অনুযায়ী)
    list_filter = ('target_lang', 'created_at', 'user')
    
    # সার্চ বার (ইউজারনেম বা টেক্সট দিয়ে খোঁজার জন্য)
    search_fields = ('user__username', 'source_text', 'translated_text')
    
    # ডেট অনুযায়ী নেভিগেশন
    date_hierarchy = 'created_at'

    # বড় টেক্সটকে ছোট করে দেখানোর জন্য একটি ফাংশন
    def source_text_short(self, obj):
        return obj.source_text[:50] + "..." if len(obj.source_text) > 50 else obj.source_text
    source_text_short.short_description = 'Source Text'