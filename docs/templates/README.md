# Templates and Examples

## Table of Contents
- [Channel Types](#channel-types)
  - [Gaming Channel](#gaming-channel)
  - [Tutorial Channel](#tutorial-channel)
  - [Vlog Channel](#vlog-channel)
  - [Educational Channel](#educational-channel)
  - [Music Channel](#music-channel)
- [CSV Templates](#csv-templates)
- [Description Templates](#description-templates)
- [Thumbnail Templates](#thumbnail-templates)
- [Advanced Examples](#advanced-examples)

## Channel Types

### Gaming Channel

#### Basic Gaming Template
```csv
file_path,title,description,tags,category,privacy_status,thumbnail_path,publish_time
gameplay/mc_ep1.mp4,"Minecraft: Epic Build! - Episode 1","🎮 Minecraft Survival Series - Episode 1

⏰ Timestamps:
0:00 - Intro
1:30 - Starting the Build
10:00 - Final Touches

👍 Leave a like if you enjoyed!
🔔 Subscribe for more content!

#minecraft #gaming #tutorial","minecraft,gaming,tutorial",20,private,thumbnails/mc_ep1.jpg,2024-02-20T15:00:00
```

#### Game Series Organization
```
gaming_channel/
├── series_1/
│   ├── episode1.mp4
│   ├── episode2.mp4
│   └── thumbnails/
├── series_2/
│   ├── episode1.mp4
│   └── thumbnails/
└── batch/
    ├── series1.csv
    └── series2.csv
```

#### Stream Highlights Template
```csv
file_path,title,description,tags,category
streams/highlight1.mp4,"BEST MOMENTS of Today's Stream! 🔥","📺 Stream Highlights

⭐ Top Moments:
${timestamps}

🎮 Games Played:
${games}

🎵 Background Music:
${music}","gaming,stream,highlights",20
```

### Tutorial Channel

#### Basic Tutorial Template
```csv
file_path,title,description,tags,category,made_for_kids,thumbnail_path,publish_time
tutorials/python1.mp4,"Python for Beginners (Part 1)","📚 Python Tutorial Series - Part 1

✨ In this video:
- Setting up Python
- Basic Syntax
- Variables and Data Types

📝 Resources:
${resources}

⏰ Timestamps:
${timestamps}

#python #programming #tutorial","python,programming,beginner",27,false,thumbnails/python1.jpg,2024-02-20T15:00:00
```

#### Course Structure
```
tutorial_channel/
├── python_course/
│   ├── module1/
│   │   ├── lesson1.mp4
│   │   └── resources/
│   └── module2/
└── batch/
    └── python_course.csv
```

#### Workshop Template
```csv
file_path,title,description,tags,publish_time
workshops/web_dev.mp4,"Web Development Workshop","🌐 Complete Web Dev Workshop

💻 What you'll learn:
- HTML Basics
- CSS Styling
- JavaScript Fundamentals

📚 Prerequisites:
- Basic computer knowledge
- Text editor installed

🔗 Resources:
${resources}","webdev,coding,workshop",2024-02-21T15:00:00
```

### Vlog Channel

#### Daily Vlog Template
```csv
file_path,title,description,tags,category,location,thumbnail_path
vlogs/daily1.mp4,"A Day in the Life - Creator Edition","📱 Daily Vlog

⏰ Today's Schedule:
${timeline}

🎵 Music Used:
${music}

🔗 Links mentioned:
${links}

📸 Instagram: @username
🐦 Twitter: @username","vlog,daily,lifestyle",22,"${location}",thumbnails/vlog1.jpg
```

#### Travel Series Template
```csv
file_path,title,description,tags,location
travel/japan1.mp4,"Japan Travel Guide: Tokyo","✈️ Japan Travel Series - Day 1

📍 Locations Visited:
${locations}

🍜 Food Spots:
${restaurants}

💰 Cost Breakdown:
${costs}

✨ Tips for Visitors:
${tips}","travel,japan,guide","Tokyo, Japan"
```

### Educational Channel

#### Lecture Series Template
```csv
file_path,title,description,tags,category,language,made_for_kids
lectures/math1.mp4,"Calculus 101 - Introduction","📚 Calculus Series - Lecture 1

📝 Topics Covered:
- Limits
- Derivatives
- Basic Functions

📖 Required Materials:
${materials}

✏️ Practice Problems:
${problems}","education,math,calculus",27,"en",false
```

#### Lab Demonstration Template
```csv
file_path,title,description,tags,safety_warning
labs/chemistry1.mp4,"Chemistry Lab: Titration","🧪 Chemistry Lab Series

⚠️ Safety First:
${safety_procedures}

🔬 Equipment Needed:
${equipment}

📝 Procedure:
${steps}

📊 Results:
${expected_results}","chemistry,lab,education","Wear safety goggles and gloves"
```

## CSV Templates

### Basic Batch Upload
```csv
file_path,title,description,tags,category,privacy_status,publish_time
videos/v1.mp4,"Title 1","Description 1","tag1,tag2",22,private,2024-02-20T15:00:00
videos/v2.mp4,"Title 2","Description 2","tag1,tag2",22,private,2024-02-21T15:00:00
```

### Advanced Batch Upload
```csv
file_path,title,description,tags,category,privacy_status,thumbnail_path,publish_time,language,made_for_kids,notify_subscribers,license
videos/v1.mp4,"Title 1","Description 1","tag1,tag2",22,private,thumbs/t1.jpg,2024-02-20T15:00:00,en,false,true,youtube
```

## Description Templates

### Gaming Video
```markdown
🎮 ${game_name} - ${episode_type} #${episode_number}

👋 Welcome back to another episode!

⏰ Timestamps:
${timestamps}

🎮 Game: ${game_name}
🎯 Version: ${game_version}
🎨 Mods Used:
${mods_list}

🔗 Useful Links:
▶️ Series Playlist: ${playlist_link}
📱 Discord: ${discord_link}
🎵 Music: ${music_credits}

#gaming #${game_tag} #letsplay
```

### Tutorial Video
```markdown
📚 ${topic} Tutorial - Part ${part_number}

In this tutorial, you'll learn:
${learning_objectives}

⏰ Timestamps:
${timestamps}

🔧 Tools Used:
${tools_list}

📝 Resources:
${resources}

❓ Questions? Join our Discord:
${discord_link}

#tutorial #${topic} #learning
```

## Thumbnail Templates

### Gaming Thumbnail
```python
thumbnail_config = {
    'background': 'game_screenshot.jpg',
    'overlay': {
        'title': {
            'text': 'EPIC WIN!',
            'position': 'center',
            'font': 'Impact',
            'size': 72
        },
        'episode': {
            'text': 'Episode 12',
            'position': 'bottom_right',
            'font': 'Arial',
            'size': 36
        }
    }
}
```

### Tutorial Thumbnail
```python
thumbnail_config = {
    'background': 'gradient_bg.jpg',
    'elements': [
        {
            'type': 'text',
            'content': 'Python Tutorial',
            'position': (540, 100)
        },
        {
            'type': 'image',
            'path': 'python_logo.png',
            'position': (540, 300)
        }
    ]
}
```

## Advanced Examples

### Multi-Series Management
```python
series_config = {
    'minecraft': {
        'upload_schedule': 'MWF',
        'time': '15:00',
        'description_template': 'templates/minecraft.md',
        'thumbnail_template': 'templates/minecraft.png'
    },
    'tutorials': {
        'upload_schedule': 'TR',
        'time': '18:00',
        'description_template': 'templates/tutorial.md',
        'thumbnail_template': 'templates/tutorial.png'
    }
}
```

### Custom End Screens
```python
end_screen_config = {
    'duration': 20,
    'elements': [
        {
            'type': 'video',
            'position': 'top_left',
            'source': 'latest'
        },
        {
            'type': 'subscribe',
            'position': 'bottom_right'
        }
    ]
}
```

For more examples and templates, check our [Community Templates](community_templates.md) and [Best Practices Guide](../best_practices.md).
