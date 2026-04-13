const BASE_URL = process.env.EXPO_PUBLIC_API_BASE_URL || 'http://127.0.0.1:5000';

if (!BASE_URL) {
  throw new Error('EXPO_PUBLIC_API_BASE_URL is not set.');
}

export async function analyzeIngredients(ingredientText, selectedProfiles) {
  const response = await fetch(`${BASE_URL}/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      ingredient_text: ingredientText,
      selected_profiles: selectedProfiles,
    }),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Failed to analyze ingredients: ${text}`);
  }

  return response.json();
}

export async function fetchProductByBarcode(barcode, selectedProfiles) {
  const params = new URLSearchParams();
  selectedProfiles.forEach((profile) => params.append('profile', profile));

  const response = await fetch(`${BASE_URL}/product/${barcode}?${params.toString()}`);

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Failed to fetch product by barcode: ${text}`);
  }

  return response.json();
}
    const text = await response.text();
    throw new Error(`Failed to fetch product by barcode: ${text}`);
  }

  return response.json();
}
