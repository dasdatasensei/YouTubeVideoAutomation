# Custom Thumbnail Examples

## Table of Contents
- [Basic Templates](#basic-templates)
- [Content-Specific Templates](#content-specific-templates)
- [Style Guidelines](#style-guidelines)
- [Technical Specifications](#technical-specifications)
- [Automation Tools](#automation-tools)

## Basic Templates

### Standard YouTube Thumbnail
```python
standard_template = {
    'dimensions': {'width': 1280, 'height': 720},
    'safe_zone': {'margin': 100},  # px from edges
    'text_area': {'max_height': 240},  # px
    'base_layers': [
        {
            'type': 'background',
            'source': 'image_or_gradient',
            'effects': ['blur', 'darken']
        },
        {
            'type': 'overlay',
            'opacity': 0.4,
            'gradient': {
                'start': '#000000',
                'end': 'transparent',
                'angle': 45
            }
        }
    ]
}
```

### Text-Focused Template
```python
text_template = {
    'background': {
        'type': 'solid_color',
        'color': '#1a1a1a'
    },
    'title': {
        'font': 'Montserrat Bold',
        'size': '72px',
        'color': '#FFFFFF',
        'shadow': {
            'color': '#000000',
            'blur': '15px',
            'distance': '10px'
        },
        'position': 'center'
    },
    'subtitle': {
        'font': 'Roboto',
        'size': '36px',
        'color': '#CCCCCC',
        'position': 'bottom_center',
        'margin_bottom': '50px'
    }
}
```

## Content-Specific Templates

### Gaming Thumbnail
```python
gaming_thumbnail = {
    'layout': 'dynamic',
    'elements': {
        'game_screenshot': {
            'position': 'full_frame',
            'effects': [
                {
                    'type': 'brightness',
                    'value': -20
                },
                {
                    'type': 'sharpen',
                    'value': 15
                }
            ]
        },
        'game_logo': {
            'position': 'top_left',
            'size': {'width': 200, 'height': 'auto'},
            'margin': 30
        },
        'episode_number': {
            'position': 'top_right',
            'font': 'Impact',
            'size': '90px',
            'color': '#FF0000',
            'stroke': {
                'color': '#FFFFFF',
                'width': '4px'
            }
        },
        'action_text': {
            'position': 'bottom_center',
            'font': 'Bebas Neue',
            'size': '120px',
            'color': '#FFFFFF',
            'stroke': {
                'color': '#000000',
                'width': '5px'
            },
            'effects': ['glow']
        }
    }
}
```

### Tutorial Thumbnail
```python
tutorial_thumbnail = {
    'layout': 'split',
    'sections': {
        'left': {
            'width': '60%',
            'content': {
                'type': 'code_screenshot',
                'language': 'python',
                'theme': 'monokai',
                'font': 'Fira Code',
                'size': '24px'
            }
        },
        'right': {
            'width': '40%',
            'background': {
                'type': 'gradient',
                'colors': ['#2C3E50', '#3498DB'],
                'angle': 135
            },
            'content': {
                'title': {
                    'font': 'Source Code Pro',
                    'size': '48px',
                    'color': '#FFFFFF',
                    'alignment': 'center',
                    'margin': '20px'
                },
                'icon': {
                    'source': 'technology_logo.png',
                    'size': '120px',
                    'position': 'center'
                }
            }
        }
    }
}
```

### Vlog Thumbnail
```python
vlog_thumbnail = {
    'layout': 'cinematic',
    'elements': {
        'hero_shot': {
            'position': 'full_frame',
            'crop': '16:9',
            'effects': [
                {
                    'type': 'color_grade',
                    'preset': 'warm_lifestyle'
                },
                {
                    'type': 'vignette',
                    'strength': 30
                }
            ]
        },
        'location_tag': {
            'position': 'top_left',
            'background': {
                'type': 'blur_box',
                'blur': '10px',
                'opacity': 0.8
            },
            'text': {
                'font': 'Playfair Display',
                'size': '36px',
                'color': '#FFFFFF',
                'padding': '10px 20px'
            }
        },
        'title_block': {
            'position': 'bottom',
            'height': '200px',
            'background': {
                'type': 'gradient',
                'colors': ['transparent', 'rgba(0,0,0,0.8)']
            },
            'text': {
                'font': 'Montserrat',
                'size': '54px',
                'color': '#FFFFFF',
                'margin': '30px'
            }
        }
    }
}
```

## Style Guidelines

### Text Hierarchy
```python
text_hierarchy = {
    'primary': {
        'font': 'Montserrat Bold',
        'size_range': {'min': '60px', 'max': '90px'},
        'color': '#FFFFFF',
        'shadow': True
    },
    'secondary': {
        'font': 'Roboto',
        'size_range': {'min': '30px', 'max': '48px'},
        'color': '#E0E0E0',
        'shadow': False
    },
    'accent': {
        'font': 'Impact',
        'size_range': {'min': '36px', 'max': '72px'},
        'color': '#FF0000',
        'stroke': True
    }
}
```

### Color Schemes
```python
color_schemes = {
    'gaming': {
        'primary': '#FF0000',
        'secondary': '#000000',
        'accent': '#FFFFFF',
        'gradients': [
            ['#FF416C', '#FF4B2B'],
            ['#000000', '#FF0000']
        ]
    },
    'tutorial': {
        'primary': '#2C3E50',
        'secondary': '#3498DB',
        'accent': '#E74C3C',
        'gradients': [
            ['#2C3E50', '#3498DB'],
            ['#2C3E50', '#2980B9']
        ]
    },
    'vlog': {
        'primary': '#FF8C00',
        'secondary': '#FFA500',
        'accent': '#FFFFFF',
        'gradients': [
            ['#FF8C00', 'transparent'],
            ['#000000', 'transparent']
        ]
    }
}
```

## Technical Specifications

### Export Settings
```python
export_settings = {
    'format': 'jpg',
    'quality': 90,
    'color_space': 'sRGB',
    'resolution': {
        'width': 1280,
        'height': 720,
        'dpi': 72
    },
    'file_size': {
        'max': '2MB',
        'compress_if_larger': True
    }
}
```

### Performance Optimization
```python
optimization_settings = {
    'image_compression': {
        'method': 'mozjpeg',
        'quality': 85,
        'target_size': '1MB'
    },
    'cache_settings': {
        'template_cache': True,
        'asset_cache': True,
        'cache_location': './thumbnail_cache'
    },
    'batch_processing': {
        'max_concurrent': 4,
        'timeout': 30  # seconds
    }
}
```

## Automation Tools

### Template Generator
```python
from PIL import Image, ImageDraw, ImageFont
import json

class ThumbnailGenerator:
    def __init__(self, template_path: str):
        with open(template_path) as f:
            self.template = json.load(f)

    def generate(self,
                content: dict,
                output_path: str):
        """Generate thumbnail from template."""
        # Implementation details...
        pass

# Usage
generator = ThumbnailGenerator('templates/gaming.json')
generator.generate({
    'title': 'Epic Gaming Moment',
    'episode': 12,
    'background': 'screenshot.jpg'
}, 'output/thumbnail.jpg')
```

### Batch Processing
```python
async def process_thumbnails(template: dict,
                           content_list: list):
    """Process multiple thumbnails concurrently."""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for content in content_list:
            task = asyncio.create_task(
                generate_thumbnail(template, content)
            )
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        return results
```

## Additional Resources
- [Advanced Template Guide](../templates/advanced.md)
- [Design Best Practices](../design/best_practices.md)
- [Performance Optimization](../optimization/performance.md)
- [Automation Guide](../automation/guide.md)
