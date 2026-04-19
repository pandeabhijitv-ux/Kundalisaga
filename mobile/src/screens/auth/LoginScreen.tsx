/**
 * Login Screen
 */

import React, {useState} from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  Alert,
} from 'react-native';
import {THEME} from '../../constants/theme';
import {useAuth} from '../../contexts/AuthContext';

const LoginScreen = ({navigation}: any) => {
  const [activeTab, setActiveTab] = useState<'password' | 'otp'>('password');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [otpEmail, setOtpEmail] = useState('');
  const [otp, setOtp] = useState('');
  const [otpSent, setOtpSent] = useState(false);
  const [generatedOtp, setGeneratedOtp] = useState('');
  const {login, loginWithOtp, continueAsGuest} = useAuth();

  const handleLogin = async () => {
    if (!email || !password) {
      Alert.alert('Error', 'Please enter email and password');
      return;
    }
    try {
      await login(email, password);
    } catch (error: any) {
      Alert.alert('Login Failed', error?.message || 'Invalid email or password');
    }
  };

  const handleSendOtp = () => {
    if (!otpEmail) {
      Alert.alert('Error', 'Please enter your email address');
      return;
    }
    const nextOtp = `${Math.floor(100000 + Math.random() * 900000)}`;
    setGeneratedOtp(nextOtp);
    setOtpSent(true);
    Alert.alert('OTP Sent', `Use OTP ${nextOtp} to continue (demo mode).`);
  };

  const handleVerifyOtp = async () => {
    if (!otp) {
      Alert.alert('Error', 'Please enter the OTP');
      return;
    }
    if (otp !== generatedOtp) {
      Alert.alert('Error', 'Invalid OTP. Please try again.');
      return;
    }
    try {
      await loginWithOtp(otpEmail);
    } catch (error: any) {
      Alert.alert('Error', error?.message || 'Login failed');
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.scrollContent}>
      <View style={styles.content}>
        <Text style={styles.titleRow}>🔒 <Text style={styles.title}>Login to KundaliSaga</Text></Text>

        {/* Tabs */}
        <View style={styles.tabContainer}>
          <TouchableOpacity
            style={[styles.tab, activeTab === 'password' && styles.activeTab]}
            onPress={() => setActiveTab('password')}>
            <Text style={[styles.tabText, activeTab === 'password' && styles.activeTabText]}>
              📧 Email & Password
            </Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.tab, activeTab === 'otp' && styles.activeTab]}
            onPress={() => setActiveTab('otp')}>
            <Text style={[styles.tabText, activeTab === 'otp' && styles.activeTabText]}>
              🔑 Email OTP
            </Text>
          </TouchableOpacity>
        </View>

        {/* Password Tab */}
        {activeTab === 'password' && (
          <View style={styles.form}>
            <Text style={styles.formTitle}>Login with Password</Text>
            <Text style={styles.fieldLabel}>Email Address</Text>
            <TextInput
              style={styles.input}
              placeholder="your@email.com"
              value={email}
              onChangeText={setEmail}
              keyboardType="email-address"
              autoCapitalize="none"
            />
            <Text style={styles.fieldLabel}>Password</Text>
            <View style={styles.passwordRow}>
              <TextInput
                style={styles.passwordInput}
                placeholder="Password"
                value={password}
                onChangeText={setPassword}
                secureTextEntry={!showPassword}
              />
              <TouchableOpacity style={styles.eyeBtn} onPress={() => setShowPassword(!showPassword)}>
                <Text style={styles.eyeIcon}>{showPassword ? '🙈' : '👁️'}</Text>
              </TouchableOpacity>
            </View>
            <View style={styles.buttonRow}>
              <TouchableOpacity style={styles.loginBtn} onPress={handleLogin}>
                <Text style={styles.loginBtnText}>Login</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={styles.registerBtn}
                onPress={() => navigation.navigate('Register')}>
                <Text style={styles.registerBtnText}>Register</Text>
              </TouchableOpacity>
            </View>
          </View>
        )}

        {/* OTP Tab */}
        {activeTab === 'otp' && (
          <View style={styles.form}>
            <Text style={styles.formTitle}>Login with OTP</Text>
            <Text style={styles.fieldLabel}>Email Address</Text>
            <TextInput
              style={styles.input}
              placeholder="your@email.com"
              value={otpEmail}
              onChangeText={setOtpEmail}
              keyboardType="email-address"
              autoCapitalize="none"
            />
            {!otpSent ? (
              <TouchableOpacity style={styles.sendOtpBtn} onPress={handleSendOtp}>
                <Text style={styles.loginBtnText}>Send OTP</Text>
              </TouchableOpacity>
            ) : (
              <>
                <Text style={styles.fieldLabel}>Enter OTP</Text>
                <TextInput
                  style={styles.input}
                  placeholder="6-digit OTP"
                  value={otp}
                  onChangeText={setOtp}
                  keyboardType="number-pad"
                  maxLength={6}
                />
                <TouchableOpacity style={styles.sendOtpBtn} onPress={handleVerifyOtp}>
                  <Text style={styles.loginBtnText}>Verify & Login</Text>
                </TouchableOpacity>
                <TouchableOpacity onPress={handleSendOtp} style={styles.resendBtn}>
                  <Text style={styles.resendText}>Resend OTP</Text>
                </TouchableOpacity>
              </>
            )}
          </View>
        )}

        {/* Divider */}
        <View style={styles.divider}>
          <View style={styles.dividerLine} />
        </View>

        {/* Guest */}
        <View style={styles.guestSection}>
          <Text style={styles.guestTitle}>Or continue as Guest</Text>
          <TouchableOpacity style={styles.guestButton} onPress={continueAsGuest}>
            <Text style={styles.guestButtonText}>🌟 Continue as Guest</Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* Footer */}
      <View style={styles.footer}>
        <Text style={styles.footerIcon}>☂️</Text>
        <Text style={styles.footerText}>Krittika Apps</Text>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFF8F0',
  },
  scrollContent: {
    flexGrow: 1,
    justifyContent: 'space-between',
  },
  content: {
    padding: 20,
    alignItems: 'center',
    marginTop: 40,
  },
  titleRow: {
    fontSize: 24,
    fontWeight: 'bold',
    color: THEME.primary,
    marginBottom: 24,
    textAlign: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: THEME.primary,
  },
  tabContainer: {
    flexDirection: 'row',
    width: '100%',
    borderBottomWidth: 1,
    borderBottomColor: '#E0E0E0',
    marginBottom: 20,
  },
  tab: {
    flex: 1,
    paddingVertical: 12,
    alignItems: 'center',
  },
  activeTab: {
    borderBottomWidth: 2,
    borderBottomColor: THEME.primary,
  },
  tabText: {
    fontSize: 14,
    color: '#888',
  },
  activeTabText: {
    color: THEME.primary,
    fontWeight: '600',
  },
  form: {
    width: '100%',
  },
  formTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 16,
  },
  fieldLabel: {
    fontSize: 13,
    color: '#555',
    marginBottom: 4,
  },
  input: {
    backgroundColor: '#F0F0F0',
    padding: 14,
    borderRadius: 8,
    marginBottom: 14,
    fontSize: 15,
    color: '#333',
  },
  passwordRow: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#F0F0F0',
    borderRadius: 8,
    marginBottom: 14,
  },
  passwordInput: {
    flex: 1,
    padding: 14,
    fontSize: 15,
    color: '#333',
  },
  eyeBtn: {
    paddingHorizontal: 12,
  },
  eyeIcon: {
    fontSize: 18,
  },
  buttonRow: {
    flexDirection: 'row',
    gap: 12,
    marginTop: 4,
  },
  loginBtn: {
    flex: 1,
    backgroundColor: 'white',
    padding: 14,
    borderRadius: 8,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#CCC',
  },
  loginBtnText: {
    color: '#333',
    fontSize: 15,
    fontWeight: '500',
  },
  registerBtn: {
    flex: 1,
    backgroundColor: 'white',
    padding: 14,
    borderRadius: 8,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#CCC',
  },
  registerBtnText: {
    color: '#333',
    fontSize: 15,
    fontWeight: '500',
  },
  sendOtpBtn: {
    backgroundColor: THEME.primary,
    padding: 14,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 4,
  },
  resendBtn: {
    alignItems: 'center',
    marginTop: 12,
  },
  resendText: {
    color: THEME.primary,
    fontSize: 14,
  },
  divider: {
    width: '100%',
    marginVertical: 24,
    flexDirection: 'row',
    alignItems: 'center',
  },
  dividerLine: {
    flex: 1,
    height: 1,
    backgroundColor: '#E0E0E0',
  },
  guestSection: {
    width: '100%',
    alignItems: 'center',
  },
  guestTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 14,
    alignSelf: 'flex-start',
  },
  guestButton: {
    width: '100%',
    padding: 14,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#E0E0E0',
    alignItems: 'center',
    backgroundColor: 'white',
  },
  guestButtonText: {
    color: '#555',
    fontSize: 15,
  },
  footer: {
    alignItems: 'center',
    paddingVertical: 24,
  },
  footerIcon: {
    fontSize: 32,
    marginBottom: 4,
  },
  footerText: {
    color: THEME.primary,
    fontSize: 14,
    fontWeight: '600',
  },
});

export default LoginScreen;
