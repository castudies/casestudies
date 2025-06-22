# Case Study Platform

A Django-based web application for creating and sharing interactive case studies with expert solutions.

## Features

- **Interactive Case Studies**: Create and share detailed case studies with background, data summary, tasks, and expert solutions
- **Image Support**: Upload thumbnails and summary images with responsive display
- **Difficulty Levels**: Categorize case studies by difficulty (Easy, Intermediate, Advanced)
- **Domain Classification**: Organize case studies by domain/topic
- **Solution Reveal**: Interactive solution reveal with confirmation modal
- **Responsive Design**: Mobile-friendly interface with Tailwind CSS
- **Admin Panel**: Easy content management through Django admin

## Technology Stack

- **Backend**: Django 5.2.3
- **Frontend**: HTML, Tailwind CSS, Alpine.js
- **Database**: SQLite (default)
- **Python**: 3.13.5

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd casestudy
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

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