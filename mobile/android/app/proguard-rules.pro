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

# Keep application class and all our custom classes
-keep class com.kundalii.saga.** { *; }
-keep interface com.kundalii.saga.** { *; }

# Keep MainApplication specifically
-keep public class com.kundalii.saga.MainApplication

# Keep MainActivity
-keep public class com.kundalii.saga.MainActivity

# Keep all native modules
-keep class com.kundalii.saga.PythonBridgeModule { *; }
-keep class com.kundalii.saga.PythonBridgePackage { *; }
