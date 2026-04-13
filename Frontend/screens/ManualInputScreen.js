import { useState } from 'react';
import {
  View, Text, StyleSheet, TextInput, Pressable, ScrollView, ActivityIndicator, Alert,
} from 'react-native';
import { analyzeIngredients } from '../services/api';

export default function ManualInputScreen({ route, navigation }) {
  const { selectedProfiles = [] } = route.params || {};
  const [ingredientText, setIngredientText] = useState('');
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!ingredientText.trim()) {
      Alert.alert('Missing Input', 'Please enter ingredient text before analysing.');
      return;
    }

    try {
      setLoading(true);

      const result = await analyzeIngredients(ingredientText, selectedProfiles);

      navigation.navigate('Results', {
        apiResult: result,
        selectedProfiles,
        ingredientText,
      });
    } catch (error) {
      Alert.alert(
        'Analysis Failed',
        'Could not analyze ingredients. Please check your connection and try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Enter Ingredients</Text>
      <Text style={styles.subtitle}>
        Paste or type the product ingredient list below
      </Text>

      <View style={styles.summaryBox}>
        <Text style={styles.summaryTitle}>Selected Profiles:</Text>
        <Text style={styles.summaryText}>
          {selectedProfiles.length > 0 ? selectedProfiles.join(', ') : 'No profiles selected'}
        </Text>
      </View>

      <TextInput
        style={styles.input}
        multiline
        placeholder="Example: Wheat flour, sugar, milk, E471"
        value={ingredientText}
        onChangeText={setIngredientText}
        textAlignVertical="top"
      />

      <Pressable
        style={[styles.primaryButton, !ingredientText.trim() && styles.disabledButton]}
        onPress={handleAnalyze}
        disabled={loading || !ingredientText.trim()}
      >
        {loading ? (
          <ActivityIndicator color="#fff" />
        ) : (
          <Text style={styles.primaryButtonText}>Analyse Ingredients</Text>
        )}
      </Pressable>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: 20, backgroundColor: '#fff', flexGrow: 1 },
  title: { fontSize: 28, fontWeight: 'bold', marginTop: 20, marginBottom: 8, textAlign: 'center' },
  subtitle: { fontSize: 16, textAlign: 'center', marginBottom: 24, color: '#444' },

  summaryBox: { marginBottom: 20, padding: 16, borderRadius: 12, backgroundColor: '#f2f2f2' },
  summaryTitle: { fontSize: 16, fontWeight: 'bold', marginBottom: 8 },
  summaryText: { fontSize: 15 },

  input: {
    minHeight: 180,
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 12,
    padding: 16,
    fontSize: 16,
    backgroundColor: '#fafafa'
  },

  primaryButton: {
    marginTop: 24,
    backgroundColor: '#222',
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center'
  },

  disabledButton: {
    backgroundColor: '#aaa'
  },

  primaryButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600'
  },
});
