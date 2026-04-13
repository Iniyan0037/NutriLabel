import { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  Pressable,
  ScrollView,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { fetchProductByBarcode } from '../services/api';

export default function ScanScreen({ route, navigation }) {
  const { selectedProfiles = [] } = route.params || {};
  const [barcode, setBarcode] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLookup = async () => {
    if (!barcode.trim()) {
      Alert.alert('Missing barcode', 'Please enter a barcode.');
      return;
    }

    try {
      setLoading(true);

      const productResult = await fetchProductByBarcode(
        barcode.trim(),
        selectedProfiles
      );

      navigation.navigate('Results', {
        apiResult: productResult.analysis,
        selectedProfiles,
        productName: productResult.product_name,
        barcode: productResult.barcode,
        ingredientText: productResult.ingredient_text,
        allergensTags: productResult.allergens_tags,
        additivesTags: productResult.additives_tags,
      });
    } catch (error) {
      Alert.alert(
        'Error',
        'Could not fetch product. Check the barcode and make sure the backend is running.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Barcode Lookup</Text>
      <Text style={styles.subtitle}>
        Enter a product barcode to fetch ingredient data from Open Food Facts
      </Text>

      <View style={styles.summaryBox}>
        <Text style={styles.summaryTitle}>Selected Profiles:</Text>
        <Text style={styles.summaryText}>
          {selectedProfiles.length > 0
            ? selectedProfiles.join(', ')
            : 'No profiles selected'}
        </Text>
      </View>

      <TextInput
        style={styles.input}
        placeholder="Example: 3017620422003"
        value={barcode}
        onChangeText={setBarcode}
        keyboardType="numeric"
      />

      <Pressable style={styles.primaryButton} onPress={handleLookup} disabled={loading}>
        {loading ? (
          <ActivityIndicator color="#fff" />
        ) : (
          <Text style={styles.primaryButtonText}>Lookup Product</Text>
        )}
      </Pressable>

      <Pressable
        style={styles.secondaryButton}
        onPress={() => navigation.navigate('ManualInput', { selectedProfiles })}
      >
        <Text style={styles.secondaryButtonText}>Enter Ingredients Manually Instead</Text>
      </Pressable>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 20,
    backgroundColor: '#fff',
    flexGrow: 1,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    marginTop: 20,
    marginBottom: 8,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 16,
    textAlign: 'center',
    marginBottom: 24,
    color: '#444',
  },
  summaryBox: {
    marginBottom: 20,
    padding: 16,
    borderRadius: 12,
    backgroundColor: '#f2f2f2',
  },
  summaryTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  summaryText: {
    fontSize: 15,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 12,
    padding: 16,
    fontSize: 16,
    backgroundColor: '#fafafa',
    marginBottom: 20,
  },
  primaryButton: {
    backgroundColor: '#222',
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
    marginBottom: 14,
  },
  primaryButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  secondaryButton: {
    borderWidth: 1,
    borderColor: '#222',
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  secondaryButtonText: {
    color: '#222',
    fontSize: 16,
    fontWeight: '600',
  },
});