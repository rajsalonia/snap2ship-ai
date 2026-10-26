# Contributing

Use an issue to propose changes to a supported template, image extraction, accessibility, or validation. Keep templates small and executable code under repository control. Model responses must remain bounded data.

1. Create a branch and install dependencies using the README.
2. Run backend tests, the dashboard production build, and `python scripts/compile_samples.py`.
3. Exercise changed interactions in the embedded preview and downloaded application.
4. Include actual validation results and limitations in your pull request.

Do not include API keys, environment files, private images, generated personal data, or provider error dumps. Use the fictional sample poster for tests and screenshots. SDK mocks belong only in tests; label curated samples in the product.
