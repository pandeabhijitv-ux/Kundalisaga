package com.kundalii.saga;

import com.facebook.react.bridge.ReactApplicationContext;
import com.facebook.react.bridge.ReactContextBaseJavaModule;
import com.facebook.react.bridge.ReactMethod;
import com.facebook.react.bridge.Promise;
import com.facebook.react.bridge.ReadableMap;
import com.facebook.react.bridge.ReadableArray;
import com.facebook.react.bridge.ReadableMapKeySetIterator;
import com.facebook.react.bridge.ReadableType;
import com.facebook.react.bridge.WritableArray;
import com.facebook.react.bridge.WritableMap;
import com.facebook.react.bridge.Arguments;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;

import org.json.JSONArray;
import org.json.JSONObject;
import org.json.JSONException;

public class PythonBridgeModule extends ReactContextBaseJavaModule {
    
    private static final String MODULE_NAME = "PythonBridge";
    
    public PythonBridgeModule(ReactApplicationContext reactContext) {
        super(reactContext);
    }
    
    @Override
    public String getName() {
        return MODULE_NAME;
    }
    
    @ReactMethod
    public void calculateChart(ReadableMap birthDetails, Promise promise) {
        try {
            Python py = Python.getInstance();
            PyObject module = py.getModule("vedic_calculator");

            String name = birthDetails.hasKey("name") ? birthDetails.getString("name") : "";
            String date = birthDetails.hasKey("date") ? birthDetails.getString("date") : "1990-01-01";
            String time = birthDetails.hasKey("time") ? birthDetails.getString("time") : "12:00";
            String location = birthDetails.hasKey("location") ? birthDetails.getString("location") : "Unknown";
            double latitude = birthDetails.hasKey("latitude") ? birthDetails.getDouble("latitude") : 0.0;
            double longitude = birthDetails.hasKey("longitude") ? birthDetails.getDouble("longitude") : 0.0;
            String timezone = birthDetails.hasKey("timezone") ? birthDetails.getString("timezone") : "Asia/Kolkata";

            PyObject result = module.callAttr(
                "calculate_chart",
                name,
                date,
                time,
                location,
                latitude,
                longitude,
                timezone
            );

            promise.resolve(jsonStringToWritableMap(result.toString()));
        } catch (Exception e) {
            promise.reject("ERROR", e.getMessage());
        }
    }
    
    @ReactMethod
    public void getRemedies(ReadableMap chartData, Promise promise) {
        try {
            Python py = Python.getInstance();
            PyObject module = py.getModule("remedy_calculator");
            String chartJson = readableMapToJsonObject(chartData).toString();
            PyObject result = module.callAttr("get_remedies", chartJson);
            promise.resolve(jsonStringToWritableMap(result.toString()));
        } catch (Exception e) {
            promise.reject("ERROR", e.getMessage());
        }
    }
    
    @ReactMethod
    public void calculateNumerology(String name, String dateOfBirth, Promise promise) {
        try {
            Python py = Python.getInstance();
            PyObject module = py.getModule("numerology_calculator");
            PyObject result = module.callAttr("calculate_numerology", name, dateOfBirth);
            promise.resolve(jsonStringToWritableMap(result.toString()));
        } catch (Exception e) {
            promise.reject("ERROR", e.getMessage());
        }
    }
    
    @ReactMethod
    public void getCurrentDasha(String dateOfBirth, Promise promise) {
        try {
            Python py = Python.getInstance();
            PyObject module = py.getModule("dasha_calculator");
            PyObject result = module.callAttr("get_current_dasha", dateOfBirth);
            promise.resolve(jsonStringToWritableMap(result.toString()));
        } catch (Exception e) {
            promise.reject("ERROR", e.getMessage());
        }
    }
    
    @ReactMethod
    public void searchKnowledgeBase(String query, Promise promise) {
        try {
            Python py = Python.getInstance();
            PyObject module = py.getModule("knowledge_search");
            PyObject result = module.callAttr("search", query);
            promise.resolve(jsonStringToWritableMap(result.toString()));
        } catch (Exception e) {
            promise.reject("ERROR", e.getMessage());
        }
    }

    @ReactMethod
    public void analyzeCareer(String chartJson, Promise promise) {
        try {
            Python py = Python.getInstance();
            PyObject module = py.getModule("career_analyzer");
            PyObject result = module.callAttr("analyze_career", chartJson);
            promise.resolve(jsonStringToWritableMap(result.toString()));
        } catch (Exception e) {
            promise.reject("ERROR", e.getMessage());
        }
    }

    @ReactMethod
    public void analyzeFinancial(String chartJson, Promise promise) {
        try {
            Python py = Python.getInstance();
            PyObject module = py.getModule("financial_analyzer");
            PyObject result = module.callAttr("analyze_financial", chartJson);
            promise.resolve(jsonStringToWritableMap(result.toString()));
        } catch (Exception e) {
            promise.reject("ERROR", e.getMessage());
        }
    }

    @ReactMethod
    public void getGemstoneRecommendations(String chartJson, String question, Promise promise) {
        try {
            Python py = Python.getInstance();
            PyObject module = py.getModule("gemstone_recommender");
            PyObject result = module.callAttr("get_gemstone_recommendations", chartJson, question);
            promise.resolve(jsonStringToWritableMap(result.toString()));
        } catch (Exception e) {
            promise.reject("ERROR", e.getMessage());
        }
    }

    @ReactMethod
    public void analyzeCompatibility(String chartAJson, String chartBJson, Promise promise) {
        try {
            Python py = Python.getInstance();
            PyObject module = py.getModule("matchmaking_analyzer");
            PyObject result = module.callAttr("analyze_compatibility", chartAJson, chartBJson);
            promise.resolve(jsonStringToWritableMap(result.toString()));
        } catch (Exception e) {
            promise.reject("ERROR", e.getMessage());
        }
    }

    @ReactMethod
    public void getMuhuratAnalysis(String chartJson, String eventType, Promise promise) {
        try {
            Python py = Python.getInstance();
            PyObject module = py.getModule("muhurat_analyzer");
            PyObject result = module.callAttr("get_muhurat_analysis", chartJson, eventType);
            promise.resolve(jsonStringToWritableMap(result.toString()));
        } catch (Exception e) {
            promise.reject("ERROR", e.getMessage());
        }
    }

    @ReactMethod
    public void analyzeVarshaphal(String chartJson, Promise promise) {
        try {
            Python py = Python.getInstance();
            PyObject module = py.getModule("varshaphal_analyzer");
            PyObject result = module.callAttr("analyze_varshaphal", chartJson);
            promise.resolve(jsonStringToWritableMap(result.toString()));
        } catch (Exception e) {
            promise.reject("ERROR", e.getMessage());
        }
    }

    @ReactMethod
    public void analyzeSoulmate(String chartJson, String gender, Promise promise) {
        try {
            Python py = Python.getInstance();
            PyObject module = py.getModule("soulmate_analyzer");
            PyObject result = module.callAttr("analyze_soulmate", chartJson, gender);
            promise.resolve(jsonStringToWritableMap(result.toString()));
        } catch (Exception e) {
            promise.reject("ERROR", e.getMessage());
        }
    }

    @ReactMethod
    public void getNameRecommendations(String chartJson, String gender, Promise promise) {
        try {
            Python py = Python.getInstance();
            PyObject module = py.getModule("name_recommender");
            PyObject result = module.callAttr("get_name_recommendations", chartJson, gender);
            promise.resolve(jsonStringToWritableMap(result.toString()));
        } catch (Exception e) {
            promise.reject("ERROR", e.getMessage());
        }
    }

    private WritableMap jsonStringToWritableMap(String jsonString) throws JSONException {
        JSONObject jsonObject = new JSONObject(jsonString);
        return jsonObjectToWritableMap(jsonObject);
    }

    private WritableMap jsonObjectToWritableMap(JSONObject jsonObject) throws JSONException {
        WritableMap map = Arguments.createMap();
        JSONArray keys = jsonObject.names();
        if (keys == null) {
            return map;
        }

        for (int i = 0; i < keys.length(); i++) {
            String key = keys.getString(i);
            Object value = jsonObject.get(key);

            if (value == JSONObject.NULL) {
                map.putNull(key);
            } else if (value instanceof JSONObject) {
                map.putMap(key, jsonObjectToWritableMap((JSONObject) value));
            } else if (value instanceof JSONArray) {
                map.putArray(key, jsonArrayToWritableArray((JSONArray) value));
            } else if (value instanceof Boolean) {
                map.putBoolean(key, (Boolean) value);
            } else if (value instanceof Integer) {
                map.putInt(key, (Integer) value);
            } else if (value instanceof Long) {
                map.putDouble(key, ((Long) value).doubleValue());
            } else if (value instanceof Double) {
                map.putDouble(key, (Double) value);
            } else {
                map.putString(key, value.toString());
            }
        }
        return map;
    }

    private WritableArray jsonArrayToWritableArray(JSONArray jsonArray) throws JSONException {
        WritableArray array = Arguments.createArray();
        for (int i = 0; i < jsonArray.length(); i++) {
            Object value = jsonArray.get(i);
            if (value == JSONObject.NULL) {
                array.pushNull();
            } else if (value instanceof JSONObject) {
                array.pushMap(jsonObjectToWritableMap((JSONObject) value));
            } else if (value instanceof JSONArray) {
                array.pushArray(jsonArrayToWritableArray((JSONArray) value));
            } else if (value instanceof Boolean) {
                array.pushBoolean((Boolean) value);
            } else if (value instanceof Integer) {
                array.pushInt((Integer) value);
            } else if (value instanceof Long) {
                array.pushDouble(((Long) value).doubleValue());
            } else if (value instanceof Double) {
                array.pushDouble((Double) value);
            } else {
                array.pushString(value.toString());
            }
        }
        return array;
    }

    private JSONObject readableMapToJsonObject(ReadableMap readableMap) throws JSONException {
        JSONObject jsonObject = new JSONObject();
        ReadableMapKeySetIterator iterator = readableMap.keySetIterator();

        while (iterator.hasNextKey()) {
            String key = iterator.nextKey();
            ReadableType type = readableMap.getType(key);

            switch (type) {
                case Null:
                    jsonObject.put(key, JSONObject.NULL);
                    break;
                case Boolean:
                    jsonObject.put(key, readableMap.getBoolean(key));
                    break;
                case Number:
                    jsonObject.put(key, readableMap.getDouble(key));
                    break;
                case String:
                    jsonObject.put(key, readableMap.getString(key));
                    break;
                case Map:
                    jsonObject.put(key, readableMapToJsonObject(readableMap.getMap(key)));
                    break;
                case Array:
                    jsonObject.put(key, readableArrayToJsonArray(readableMap.getArray(key)));
                    break;
            }
        }

        return jsonObject;
    }

    private JSONArray readableArrayToJsonArray(ReadableArray readableArray) throws JSONException {
        JSONArray jsonArray = new JSONArray();

        for (int i = 0; i < readableArray.size(); i++) {
            ReadableType type = readableArray.getType(i);
            switch (type) {
                case Null:
                    jsonArray.put(JSONObject.NULL);
                    break;
                case Boolean:
                    jsonArray.put(readableArray.getBoolean(i));
                    break;
                case Number:
                    jsonArray.put(readableArray.getDouble(i));
                    break;
                case String:
                    jsonArray.put(readableArray.getString(i));
                    break;
                case Map:
                    jsonArray.put(readableMapToJsonObject(readableArray.getMap(i)));
                    break;
                case Array:
                    jsonArray.put(readableArrayToJsonArray(readableArray.getArray(i)));
                    break;
            }
        }

        return jsonArray;
    }
}
