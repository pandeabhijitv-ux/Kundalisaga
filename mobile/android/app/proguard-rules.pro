# Add project specific ProGuard rules here.

# Keep React Native classes
-keep class com.facebook.react.** { *; }
-keep class com.facebook.jni.** { *; }

# Keep Chaquopy Python classes
-keep class com.chaquo.python.** { *; }

# Keep native methods
-keepclasseswithmembernames class * {
    native <methods>;
}

# Keep Hermes classes
-keep class com.facebook.hermes.unicode.** { *; }
-keep class com.facebook.jni.** { *; }

# React Native
-dontwarn com.facebook.react.**
-dontwarn okhttp3.**
-dontwarn okio.**

# Keep Android support classes  
-keep class androidx.** { *; }
-keep interface androidx.** { *; }

# Keep application class
-keep class com.kundalii.saga.MainApplication { *; }
