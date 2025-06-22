# CaseStudies

A Django-based platform for curating and presenting real-world business case studies to help professionals, students, and decision-makers understand complex business challenges and their solutions.

## Features

- **Case Study Library**: Browse and search through a curated collection of real business cases
- **Search Functionality**: Discover case studies by title, domain, or difficulty level
- **Responsive Design**: Modern, mobile-friendly interface built with Tailwind CSS
- **About Page**: Learn about the platform's mission and creator
- **Legal Pages**: Comprehensive Terms of Service and Privacy Policy

## Pages

### Main Pages
- **Home** (`/`): Landing page with featured case studies
- **Cases** (`/cases/`): Complete list of all case studies with search functionality
- **Case Study Detail** (`/<slug>/`): Individual case study pages

### Information Pages
- **About** (`/about/`): Platform mission, creator information, and support options
- **Terms of Service** (`/terms/`): Legal terms and conditions for using the platform
- **Privacy Policy** (`/privacy/`): How we collect, use, and protect your information

## Technology Stack

- **Backend**: Django 4.x
- **Frontend**: Tailwind CSS, Alpine.js
- **Database**: SQLite (default)
- **Icons**: Heroicons (SVG)
- **Fonts**: Epilogue (Google Fonts)

## Design System

The website follows a consistent design pattern:
- **Colors**: Black header with white text, white content areas with black text
- **Typography**: Epilogue font family with various weights
- **Layout**: Responsive grid system with rounded corners and borders
- **Interactive Elements**: Hover effects with shadow and transform animations
- **Primary Color**: #4285f2 (blue)

## Creator

**Mushfikur Rahman Mahi**
- Twitter: [@mushfikurahmaan](https://x.com/mushfikurahmaan)
- LinkedIn: [mushfikrahman](https://www.linkedin.com/in/mushfikrahman/)
- Support: [Buy me a coffee](https://ko-fi.com/mushfikurahmaan)

## Getting Started

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Create a superuser: `python manage.py createsuperuser`
5. Run the development server: `python manage.py runserver`
6. Visit `http://localhost:8000`

## License

This project is for educational and informational purposes. Please refer to the Terms of Service and Privacy Policy for detailed usage guidelines.

## Project Structure

```
casestudy/
├── casestudies/          # Main app
│   ├── models.py         # CaseStudy model
│   ├── views.py          # View logic
│   ├── urls.py           # URL routing
│   ├── admin.py          # Admin configuration
│   └── templates/        # HTML templates
├── casestudy_project/    # Django project settings
├── media/               # Uploaded files
├── assets/              # Static assets
└── requirements.txt     # Python dependencies
```

## Usage

### Creating Case Studies

1. Access the admin panel at `/admin/`
2. Navigate to "Case Studies" section
3. Click "Add Case Study"
4. Fill in the required fields:
   - **Title**: Case study title
   - **Thumbnail**: Main image (370x160px recommended)
   - **Difficulty**: Easy, Intermediate, or Advanced
   - **Domain**: Topic area
   - **Case Background**: Problem description
   - **Data Summary**: Data overview and context
   - **Summary Images**: Additional images (384x256px recommended)
   - **Task**: What needs to be solved
   - **Expert Solution**: Complete solution (hidden by default)

### Image Guidelines

- **Thumbnail**: 370px wide × 160px tall
- **Summary Images**: 384px wide × 256px (3:2 or 4:3 aspect ratio)
- **Format**: JPEG or PNG
- **File Size**: Keep under 500KB for optimal performance

## Development

### Adding New Features

1. Create new migrations for model changes:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. Update templates in `casestudies/templates/casestudies/`

3. Modify views in `casestudies/views.py`

### Customization

- **Styling**: Modify Tailwind classes in templates
- **Functionality**: Extend Alpine.js components
- **Models**: Add new fields to `CaseStudy` model

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For questions or issues, please open an issue on the repository. 