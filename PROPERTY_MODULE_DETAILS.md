# Property Module Details

This document provides a comprehensive overview of the Property module within the Kenyan Rental Management System. It details the data structure of a `Property`, including its attributes, enumerations for type and status, and how location and other key features are stored. Furthermore, it outlines how different user roles, with a special focus on landlord operations, interact with the Property module via API endpoints and system functionalities. The information herein is primarily based on the data model found in `rental_management_mvp/models/property.py` and relevant route definitions.

## 1. `Property` Class Attributes

This section describes the attributes of the `Property` class.

| Name                  | Data Type                     | Purpose/Description                                                                 | Mandatory/Optional | Default Value             |
|-----------------------|-------------------------------|-------------------------------------------------------------------------------------|--------------------|---------------------------|
| `property_id`         | `int`                         | Unique identifier for the property.                                                 | Mandatory          | None                      |
| `landlord_id`         | `int`                         | Foreign Key to the `User` object, identifying the landlord who owns the property.   | Mandatory          | None                      |
| `address_line_1`      | `str`                         | Main street address, plot number, or building name.                                 | Mandatory          | None                      |
| `city`                | `str`                         | Major town or city where the property is located (e.g., Nairobi, Mombasa).          | Mandatory          | None                      |
| `county`              | `str`                         | County where the property is located (e.g., "Nairobi County"). Marked as indexed.   | Mandatory          | None                      |
| `property_type`       | `PropertyType`                | The type of property (e.g., `APARTMENT_UNIT`, `TOWNHOUSE`).                         | Mandatory          | None                      |
| `num_bedrooms`        | `int`                         | Number of bedrooms. Use 0 for property types where not applicable (e.g., bedsitters). | Mandatory          | None                      |
| `num_bathrooms`       | `int`                         | Number of bathrooms.                                                                | Mandatory          | None                      |
| `unit_number`         | `Optional[str]`               | Specific unit identifier (e.g., "A5", "Shop 3"). Consider for legacy or simple cases. Marked as indexed. | Optional           | `None`                    |
| `unit_name`           | `Optional[str]`               | Descriptive name for the unit (e.g., "Penthouse A", "Ground Floor Shop"). Marked as indexed. | Optional           | `None`                    |
| `building_name`       | `Optional[str]`               | Name of the building or complex (e.g., "Sunrise Towers", "Westwood Mall"). Marked as indexed. | Optional           | `None`                    |
| `estate_neighborhood` | `Optional[str]`               | Specific estate or neighborhood (e.g., "Kilimani"). Marked as indexed.              | Optional           | `None`                    |
| `ward`                | `Optional[str]`               | Administrative ward (e.g., "Parklands/Highridge"). Marked as indexed.               | Optional           | `None`                    |
| `sub_county`          | `Optional[str]`               | Sub-county (e.g., "Westlands"). Marked as indexed.                                  | Optional           | `None`                    |
| `address_line_2`      | `Optional[str]`               | Additional address details (e.g., floor, if not covered by `unit_name` or `building_name`). | Optional           | `None`                    |
| `postal_code`         | `Optional[str]`               | Postal code for the address.                                                        | Optional           | `None`                    |
| `size_sqft`           | `Optional[int]`               | Size of the property in square feet.                                                | Optional           | `None`                    |
| `amenities`           | `Optional[List[str]]`         | List of text strings for amenities (e.g., `"BOREHOLE_WATER"`, `"GYM"`).             | Optional           | `[]` (empty list)         |
| `photos_urls`         | `Optional[List[str]]`         | List of URLs pointing to images of the property.                                    | Optional           | `[]` (empty list)         |
| `main_photo_url`      | `Optional[str]`               | URL of the primary photo for the property.                                          | Optional           | `None`                    |
| `description`         | `Optional[str]`               | Detailed textual description of the property.                                       | Optional           | `None`                    |
| `status`              | `PropertyStatus`              | Current status of the property (e.g., `VACANT`, `OCCUPIED`).                        | Optional           | `PropertyStatus.VACANT`   |
| `created_at`          | `datetime`                    | Timestamp of when the property record was created.                                  | Optional           | `datetime.utcnow()`       |
| `updated_at`          | `datetime`                    | Timestamp of when the property record was last updated.                             | Optional           | `datetime.utcnow()`       |

## 2. `PropertyType` Enum

This enumeration defines the different types of properties that can be managed.

| Value                 | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| `APARTMENT_UNIT`      | A unit within a larger apartment block.                                     |
| `BEDSITTER`           | Typically a single room combining living, sleeping, and cooking areas, with a separate bathroom. |
| `SINGLE_ROOM`         | A single room unit, often with shared facilities.                           |
| `STUDIO_APARTMENT`    | Similar to a bedsitter, an open-plan living space, potentially more distinct or larger. |
| `TOWNHOUSE`           | A multi-floor residential unit, often sharing walls with adjacent units.    |
| `MAISONETTE`          | A self-contained unit, typically with its own entrance, often part of a larger complex. |
| `BUNGALOW`            | A single-story house, usually detached.                                     |
| `OWN_COMPOUND_HOUSE`  | A standalone house within its own private compound/yard.                    |
| `COMMERCIAL_PROPERTY` | Property intended for business use (e.g., shop, office).                    |

## 3. `PropertyStatus` Enum

This enumeration defines the current status of a property.

| Value               | Description                                                                    |
|---------------------|--------------------------------------------------------------------------------|
| `VACANT`            | The property is currently empty and available.                                 |
| `OCCUPIED`          | The property is currently occupied.                                            |
| `UNDER_MAINTENANCE` | The property is currently undergoing maintenance and is not available.         |

## 4. Location Data Structure

The property's location is stored using a combination of structured and flexible address fields:

*   **Street/Building:** `address_line_1` (e.g., "Ngong Road", "Moi Avenue"). This is the primary street address.
*   **Building Name:** `building_name` (e.g., "Sunshine Apartments", "Reliable Towers"). Specifies the name of the building complex if applicable.
*   **Unit Name:** `unit_name` (e.g., "Penthouse B", "Suite 203", "Shop G5"). Describes the specific unit within a building.
*   **Unit Number:** `unit_number` (e.g., "A5", "10B"). Can be used for legacy data or simple numbering systems, complements `unit_name`.
*   **Additional Address Details:** `address_line_2` can store further details like floor number if not part of `unit_name`, or specific block details within a larger unnamed complex.
*   **City:** `city` (e.g., "Nairobi").
*   **County:** `county` (e.g., "Nairobi County").
*   **Sub-County:** `sub_county` (e.g., "Westlands").
*   **Ward:** `ward` (e.g., "Parklands/Highridge").
*   **Estate/Neighborhood:** `estate_neighborhood` (e.g., "Kilimani", "Lavington").
*   **Postal Code:** `postal_code`.

**Indexed Fields for Location:**
The following fields are designed to be indexed for efficient searching:
*   `unit_number`
*   `unit_name`
*   `building_name`
*   `county`
*   `estate_neighborhood`
*   `ward`
*   `sub_county`

## 5. Storage of Other Key Features

*   **Size:**
    *   `size_sqft`: Stored as an `Optional[int]`, representing the property area in square feet.
*   **Amenities:**
    *   `amenities`: Stored as an `Optional[List[str]]`. This is a list of text strings (e.g., `"BOREHOLE_WATER"`, `"ELECTRIC_FENCE"`). Defaults to an empty list.
*   **Photos:**
    *   `photos_urls`: Stored as an `Optional[List[str]]`. A list of URLs for property images. Defaults to an empty list.
    *   `main_photo_url`: Stored as an `Optional[str]`. A single URL for the primary property photo.

## 6. Landlord Interactions with Property Module (API Endpoints)

This section details how authenticated landlords interact with the property module via API endpoints. It prioritizes Phase 1 MVP features and supplements with advanced capabilities from later phases.

### 6.1. Creating a New Property
*   **Endpoint:** `POST /properties`
*   **Purpose:** Allows a landlord to create a new property record.
*   **Required Fields (Phase 1 MVP):**
    *   `address_line_1` (str)
    *   `city` (str)
    *   `county` (str)
    *   `property_type` (str, from `PropertyType` enum)
    *   `num_bedrooms` (int)
    *   `num_bathrooms` (int)
*   **Optional Fields (Phase 1 MVP):**
    *   `unit_number` (str), `unit_name` (str), `building_name` (str), `estate_neighborhood` (str), `ward` (str), `sub_county` (str), `address_line_2` (str), `postal_code` (str)
    *   `size_sqft` (int)
    *   `amenities` (List[str])
    *   `main_photo_url` (str, URL), `photos_urls` (List[str], URLs)
    *   `description` (str)
    *   `status` (str, from `PropertyStatus` enum, defaults to `VACANT`)
*   **Later Phase Considerations:**
    *   Phase 4: Public listing fields (e.g., `public_listing_description`) can also be set.
    *   Phase 6: `Property.syndication_settings` might be initialized.
*   **Expected Response:** Full property details of the new property, including its `property_id`.

### 6.2. Listing Landlord Properties
*   **Endpoint:** `GET /properties`
*   **Purpose:** Allows a landlord to retrieve a list of their properties.
*   **Pagination:** Supported.
*   **Expected Response:** A paginated list of property summaries (e.g., `property_id`, `address_line_1`, `status`).

### 6.3. Getting Specific Property Details
*   **Endpoint:** `GET /properties/{property_id}`
*   **Purpose:** Allows a landlord to retrieve comprehensive details for a specific owned property.
*   **Ownership Check:** Ensures the property belongs to the authenticated landlord.
*   **Expected Response:** Full property details. Later phases may include public listing and syndication settings.

### 6.4. Updating Core Property Details
*   **Endpoint:** `PUT /properties/{property_id}`
*   **Purpose:** Allows a landlord to update core information of an owned property.
*   **Ownership Check:** Ensures property belongs to the landlord.
*   **Fields that can be updated:** Generally, any field settable during creation (see 6.1), including `status`.
*   **Later Phase Considerations:** Excludes specific public listing fields (see 6.8) and direct syndication settings.
*   **Expected Response:** Full updated property details.

### 6.5. Managing Property Photos
*   **Upload Endpoint:** `POST /properties/{property_id}/photos`
*   **Purpose:** Allows a landlord to upload photos (using `multipart/form-data`).
*   **Association:** Uploaded photo URLs are added to `Property.photos_urls`. `Property.main_photo_url` is updated via the `PUT /properties/{property_id}` endpoint.
*   **Expected Response (for photo upload):** Updated list of `photos_urls`.

### 6.6. Managing Property Status
*   **How status is updated:** The `Property.status` field (e.g., `VACANT`, `OCCUPIED`) is updated via the `PUT /properties/{property_id}` endpoint.

### 6.7. Deleting a Property
*   **Endpoint:** `DELETE /properties/{property_id}`
*   **Purpose:** Allows a landlord to delete an owned property.
*   **Ownership Check:** Required.
*   **Considerations:** Implications for active leases must be handled (e.g., prevent deletion or archive).
*   **Expected Response:** Success message or `204 No Content`.

### 6.8. Managing Public Vacancy Listings (Phase 4+ features)
*   **Endpoint:** `PUT /properties/{property_id}/listing-details`
*   **Purpose:** Allows a landlord to manage public advertisement details for a vacant property.
*   **Fields:** `public_listing_description` (str), `is_publicly_listed` (bool), `vacancy_listing_url_slug` (str), etc.
*   **Expected Response:** Updated listing details or full property details. May trigger syndication updates.

### 6.9. Property Syndication (Phase 6+ considerations)
*   **Settings Management:** `Property.syndication_settings` (JSON) can be initialized at creation or updated via listing detail updates, influencing external platform syndication. Direct syndication actions are typically separate.

## 7. Other User Interactions with Property Module

This section details how users other than landlords interact with property information.

### 7.1. Prospective Tenant Interactions (Public Access - Phase 4+)

Unauthenticated users can find available rental properties.

*   **Listing Public Vacancies:**
    *   **Endpoint:** `GET /public/properties`
    *   **Purpose:** Search and view publicly listed vacant properties. Supports filtering.
    *   **Expected Response:** List of public property summaries (address, rent, main photo, `vacancy_listing_url_slug`).

*   **Viewing a Single Public Vacancy:**
    *   **Endpoint:** `GET /public/properties/{vacancy_listing_url_slug}`
    *   **Purpose:** View detailed information for a specific public listing.
    *   **Expected Response:** Detailed public property information, excluding sensitive landlord data.

*   **Submitting an Inquiry:**
    *   **Endpoint:** `POST /public/properties/{property_id}/inquire`
    *   **Purpose:** Express interest and submit an inquiry (contact info, message). Creates a `ProspectInquiry` record.
    *   **Expected Response:** Confirmation of submission.

### 7.2. Tenant Interactions (Authenticated)

Active tenants interact with property information relevant to their lease.

*   **Viewing Leased Property Details:**
    *   **Access:** Via tenant dashboard or lease-specific sections.
    *   **Information:** Core property details, landlord/manager contact (possibly masked), lease documents.
    *   **Purpose:** Provide tenants with necessary information about their rented space. Tenants do not modify property details.

### 7.3. System Administrator Interactions (Authenticated, Privileged)

System Administrators have broad access for platform management and support.

*   **Access:** Via dedicated admin interfaces/APIs (e.g., `/api/v1/admin/properties`).
*   **Functions:**
    *   **Viewing/Managing Any Property:** For troubleshooting, data correction, compliance, or support. Can view/edit all details.
    *   **Platform Configuration:** Manage global property-related settings (e.g., amenity lists if configurable).
    *   **Deactivation/Archival:** Assist in property deactivation/archival.
    *   **Audit and Oversight:** Review property-related activities.

This document provides a foundational understanding of the Property module, its data definitions, and its operational interactions across various user roles within the system.
