# PixelPersona API Documentation

## Overview

The PixelPersona API provides endpoints for generating avatars and converting images to ASCII art.

## Base URL

```
/api/v1
```

## Endpoints

### Generate Avatar

Generate a unique avatar based on a name/nickname.

```
POST /avatar
```

**Request Body:**
```json
{
  "name": "string",
  "style": "Monster|Robot|Planet",
  "symmetry": "Vertical|Horizontal|Radial|Grid",
  "width": "integer (optional, default: 32)",
  "height": "integer (optional, default: 32)"
}
```

**Response:**
```json
{
  "svg": "string (SVG content)",
  "seed": "integer (generated seed)"
}
```

### Convert Image to ASCII Art

Convert an uploaded image to stylized ASCII art.

```
POST /ascii
```

**Request Body (multipart/form-data):**
```
image: file (PNG, JPG, SVG, WebP)
theme: string (Retro|Cyberpunk|Nature|Braille)
width: integer (optional, default: 64)
height: integer (optional, default: 64)
dithering: boolean (optional, default: false)
```

**Response:**
```json
{
  "ascii": "string (ASCII art content)",
  "config": "object (used configuration)"
}
```

### Export

Export generated content to various formats.

```
POST /export
```

**Request Body:**
```json
{
  "content": "string",
  "format": "txt|ans|svg|png|json",
  "config": "object (optional, export configuration)"
}
```

**Response:**
File content in the requested format.