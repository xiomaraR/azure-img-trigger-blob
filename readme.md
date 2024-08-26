### Project Overview

This Azure Function app is designed to process images uploaded to a specified blob container. When an image is added, the function triggers, analyzes the image using Azure Vision AI, and extracts key information like:

- Description
- Tags
- Objects
- Colors
- Clip/line art classification

### Azure Resources

- **Azure Function App:** The core component that executes the function logic.
- **Blob Storage:** Used to store the images and trigger the function.
- **Azure Vision AI:** Provides the image analysis capabilities.

**Note:** For more instructions on setting up and configuring these resources, refer to the official Azure documentation.
