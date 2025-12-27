# HueVault

A comprehensive design tool for graphic designers at every stage of their workflow. HueVault provides color palette generation, color accessibility testing, SVG conversion, background removal, and public project portfolio pages.

## Features

### 🎨 Color Palette Generator
- Interactive palette generation with customizable parameters
- Slider controls for Formal ↔ Playful and Modern ↔ Classic
- Multi-select adjectives (youthful, enterprise, modern, luxury, gaudy, pastel, monotone, muted)
- Manual color input support
- Lock individual colors and regenerate only unlocked ones
- Expand palette size dynamically
- Copy hex values to clipboard

### 👁️ Color Accessibility & Color-Blindness Simulator
- Visual comparison tool (not a pass/fail checker)
- Simulates three types of color vision deficiencies:
  - Protanopia (Red-blind)
  - Deuteranopia (Green-blind)
  - Tritanopia (Blue-blind)
- Side-by-side comparisons of original and simulated palettes
- Deterministic, rule-based color space transformations

### 🖼️ SVG Converter
- Convert SVG files to high-resolution raster formats
- Output formats: PNG, JPEG, TIFF
- Resolution: 1200 DPI
- Preserves transparency where applicable

### ✂️ Background Removal Tool
- Remove solid background colors from images
- Supports PNG, JPEG, and TIFF formats
- Color picker and hex input for background color selection
- Adjustable color tolerance
- Outputs with transparent background

### 📁 Public Project Pages
- Create public-facing portfolio pages
- Display color palettes, logos, favicons, and graphics
- Clean gallery layout
- No authentication required

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone or download the repository**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Project Structure

```
HueVault/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── blueprints/            # Flask blueprints (modular routes)
│   ├── __init__.py
│   ├── main.py            # Home page
│   ├── palette.py         # Color palette generator
│   ├── accessibility.py   # Color-blindness simulator
│   ├── svg_converter.py   # SVG conversion tool
│   ├── background_removal.py  # Background removal tool
│   └── projects.py        # Project pages
├── utils/                 # Utility modules
│   ├── __init__.py
│   ├── color_utils.py     # Color palette generation logic
│   ├── colorblind_simulator.py  # Color-blindness simulation
│   └── image_utils.py     # Image processing utilities
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── index.html         # Home page
│   ├── palette.html       # Palette generator page
│   ├── accessibility.html # Accessibility tool page
│   ├── svg_converter.html # SVG converter page
│   ├── background_removal.html  # Background removal page
│   ├── projects.html      # Projects list page
│   ├── create_project.html # Create project page
│   ├── project_view.html  # Individual project page
│   └── error.html         # Error page
├── static/                # Static assets
│   ├── css/               # Stylesheets
│   │   ├── main.css       # Main styles
│   │   ├── palette.css    # Palette generator styles
│   │   ├── accessibility.css  # Accessibility tool styles
│   │   ├── tools.css      # Tool pages styles
│   │   └── projects.css   # Projects pages styles
│   ├── js/                # JavaScript files
│   │   ├── main.js        # General utilities
│   │   ├── palette.js     # Palette generator logic
│   │   ├── accessibility.js  # Accessibility tool logic
│   │   ├── svg_converter.js  # SVG converter logic
│   │   ├── background_removal.js  # Background removal logic
│   │   └── create_project.js  # Project creation logic
│   ├── logo.png           # HueVault logo
│   └── favicon.png        # Browser favicon
├── graphics/              # Original graphics files
│   ├── Logo - HueVault.png
│   └── Favicon - HueVault.png
├── uploads/               # Temporary file uploads (auto-created)
├── projects/              # Project data storage (auto-created)
└── static/outputs/        # Output files (auto-created)
```

## Usage

### Color Palette Generator

1. Navigate to the Palette Generator page
2. Set the number of colors you want
3. Adjust the Formal ↔ Playful and Modern ↔ Classic sliders
4. Select relevant adjectives
5. Optionally add manual color inputs
6. Click "Generate Palette"
7. Lock colors you want to keep and regenerate others
8. Expand the palette if needed

### Color Accessibility Tool

1. Navigate to the Accessibility page
2. Enter hex colors separated by commas (or paste from Palette Generator)
3. Click "Load Palette"
4. View side-by-side comparisons of how the palette appears with different color vision deficiencies

### SVG Converter

1. Navigate to the SVG Converter page
2. Select an SVG file
3. Choose output format (PNG, JPEG, or TIFF)
4. Click "Convert"
5. The converted file will download automatically at 1200 DPI

### Background Removal

1. Navigate to the Background Removal page
2. Upload an image (PNG, JPEG, or TIFF)
3. Select or enter the background color to remove
4. Adjust tolerance if needed
5. Click "Remove Background"
6. The processed image will download automatically

### Project Pages

1. Navigate to Projects
2. Click "Create New Project"
3. Fill in project details, palettes, and asset URLs
4. Save to create a public project page
5. Share the project URL

## Technical Details

### Color Palette Generation
- Deterministic, rule-based algorithm (no machine learning)
- Uses HSV color space for intuitive color manipulation
- Adjective-based hue selection
- Slider-based saturation and value adjustment

### Color-Blindness Simulation
- Based on cone-response color space (LMS)
- Uses Bradford transformation matrix
- Deterministic color space conversions
- Fast, client-side or server-side processing

### Image Processing
- Uses Pillow (PIL) for image manipulation
- CairoSVG for SVG to raster conversion
- High-resolution output (1200 DPI)
- Preserves transparency where applicable

## Design Philosophy

- **Modern & Minimalist**: Clean, whitespace-forward design
- **Designer-Focused**: Tools built for real design workflows
- **IBM Color Palette**: Professional accent colors
- **Responsive**: Desktop-first, mobile-friendly
- **Modular**: Easy to extend with new features

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Modern mobile browsers

## Development

### Running in Development Mode

The app runs in debug mode by default when executed with `python app.py`. For production, set environment variables:

```bash
export SECRET_KEY='your-secret-key-here'
export FLASK_ENV=production
```

### Adding New Features

The application uses Flask blueprints for modularity. To add a new feature:

1. Create a new blueprint in `blueprints/`
2. Register it in `app.py`
3. Create corresponding templates and static assets
4. Add navigation links in `templates/base.html`

## License

This project is provided as-is for educational and personal use.

## Notes

- No authentication is implemented (as per requirements)
- File uploads are stored temporarily and cleaned up after processing
- Projects are stored as JSON files locally
- All algorithms are deterministic (no ML/AI)
- The application is designed to be easily extended with authentication, cloud storage, etc.

## Troubleshooting

### Import Errors
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### File Upload Issues
Ensure the `uploads/` directory exists and is writable.

### SVG Conversion Errors
Make sure CairoSVG dependencies are installed. On Windows, you may need additional system libraries.

### Port Already in Use
Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## Future Enhancements

Potential features for future development:
- User authentication and accounts
- Cloud storage integration
- Export palettes to various formats (Adobe Swatch, CSS, etc.)
- Advanced color harmony algorithms
- Batch processing for image tools
- Project templates
- Collaboration features

