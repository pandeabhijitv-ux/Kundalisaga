package com.kundalii.saga;

import com.facebook.react.bridge.ReactApplicationContext;
import com.facebook.react.bridge.ReactContextBaseJavaModule;
import com.facebook.react.bridge.ReactMethod;
import com.facebook.react.bridge.Promise;
import com.facebook.react.bridge.ReadableMap;
import com.facebook.react.bridge.WritableMap;
import com.facebook.react.bridge.WritableNativeMap;
import com.facebook.react.bridge.WritableArray;
import com.facebook.react.bridge.WritableNativeArray;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;

import org.json.JSONObject;
import org.json.JSONArray;

public class PythonBridgeModule extends ReactContextBaseJavaModule {
    private Python py;

    PythonBridgeModule(ReactApplicationContext context) {
        super(context);
        py = Python.getInstance();
    }

    @Override
    public String getName() {
        return "PythonBridge";
    }

    /**
     * Calculate Vedic Birth Chart
     */
    @ReactMethod
    public void calculateChart(ReadableMap birthDetails, Promise promise) {
        try {
            PyObject vedicModule = py.getModule("vedic_calculator");
            
            // Convert ReadableMap to Python dict
            String name = birthDetails.getString("name");
            String dateStr = birthDetails.getString("date");
            String timeStr = birthDetails.getString("time");
            String location = birthDetails.getString("location");
            double latitude = birthDetails.getDouble("latitude");
            double longitude = birthDetails.getDouble("longitude");
            String timezone = birthDetails.getString("timezone");
            
            // Call Python function
            PyObject result = vedicModule.callAttr("calculate_chart",
                name, dateStr, timeStr, location, latitude, longitude, timezone);
            
            // Convert Python result to JSON string and parse it
            String jsonResult = result.toString();
            WritableMap chartData = convertJsonToMap(jsonResult);
            
            promise.resolve(chartData);
        } catch (Exception e) {
            promise.reject("CALCULATE_CHART_ERROR", e.getMessage());
        }
    }

    /**
     * Get Remedies for chart
     */
    @ReactMethod
    public void getRemedies(ReadableMap chartData, Promise promise) {
        try {
            PyObject remedyModule = py.getModule("remedy_calculator");
            
            // Convert chart data to JSON string
            String chartJson = convertMapToJson(chartData);
            
            // Call Python function
            PyObject result = remedyModule.callAttr("get_remedies", chartJson);
            
            // Convert result
            WritableMap remedies = convertJsonToMap(result.toString());
            promise.resolve(remedies);
        } catch (Exception e) {
            promise.reject("GET_REMEDIES_ERROR", e.getMessage());
        }
    }

    /**
     * Calculate Numerology
     */
    @ReactMethod
    public void calculateNumerology(String name, String dateOfBirth, Promise promise) {
        try {
            PyObject numerologyModule = py.getModule("numerology_calculator");
            PyObject result = numerologyModule.callAttr("calculate_numerology", name, dateOfBirth);
            
            WritableMap numerologyData = convertJsonToMap(result.toString());
            promise.resolve(numerologyData);
        } catch (Exception e) {
            promise.reject("NUMEROLOGY_ERROR", e.getMessage());
        }
    }

    /**
     * Get Current Dasha periods
     */
    @ReactMethod
    public void getCurrentDasha(String dateOfBirth, Promise promise) {
        try {
            PyObject dashaModule = py.getModule("dasha_calculator");
            PyObject result = dashaModule.callAttr("get_current_dasha", dateOfBirth);
            
            WritableMap dashaData = convertJsonToMap(result.toString());
            promise.resolve(dashaData);
        } catch (Exception e) {
            promise.reject("DASHA_ERROR", e.getMessage());
        }
    }

    /**
     * Search Knowledge Base
     */
    @ReactMethod
    public void searchKnowledge(String query, Promise promise) {
        try {
            PyObject knowledgeModule = py.getModule("knowledge_search");
            PyObject result = knowledgeModule.callAttr("search", query);
            
            WritableMap searchResults = convertJsonToMap(result.toString());
            promise.resolve(searchResults);
        } catch (Exception e) {
            promise.reject("KNOWLEDGE_SEARCH_ERROR", e.getMessage());
        }
    }

    // Helper method to convert JSON string to WritableMap
    private WritableMap convertJsonToMap(String jsonStr) throws Exception {
        WritableNativeMap map = new WritableNativeMap();
        JSONObject jsonObject = new JSONObject(jsonStr);
        
        // Add your JSON parsing logic here
        // This is a simplified version
        return map;
    }

    // Helper method to convert ReadableMap to JSON string
    private String convertMapToJson(ReadableMap map) {
        // Add your conversion logic here
        return "{}";
    }
}
