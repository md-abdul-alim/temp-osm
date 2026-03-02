# Order Management System (OSM)

A minimal Django REST Framework (DRF) project for managing customers, variants, and orders with automated spending tracking.

## Features
- **Order Creation**: Validate prices against cost price and track spending.
- **Spending Tracking**: Signals automatically update `customer.total_spent` on item creation and deletion.
- **Reports**: Quick customer spending summaries.
- **Service/Selector Pattern**: Clean separation of business logic and data fetching.

## Setup Instructions

### Prerequisites
- Python 3.10+
- `pip`

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd temp-osm
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install django djangorestframework
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

### Running Tests
To verify the implementation and signal logic:
```bash
python manage.py test orders
```

## API Endpoints

All API endpoints are prefixed with `/api/`.

### Orders

#### 1. Create Order
- **URL:** `POST /api/orders/create/`
- **Body:**
  ```json
  {
      "customer_id": 1,
      "items": [
          {
              "variant_id": 1,
              "quantity": 2,
              "price": "150.00"
          }
      ]
  }
  ```
- **Validation:** Fails if `price` is below the variant's `cost_price`.

#### 2. Order Detail
- **URL:** `GET /api/orders/<int:pk>/`
- **Description:** Returns order summary, total amount, and all items.

### Customers

#### 3. Customer Spending Report
- **URL:** `GET /api/customers/<int:pk>/report/`
- **Description:** Shows the total amount the customer has spent across all orders.

## Project Structure
- `services.py`: Atomic transactions and data modification logic.
- `selectors.py`: Optimized data fetching using `select_related` and `prefetch_related`.
- `signals.py`: Automated updates for `total_spent` field.
- `serializers.py`: Custom logic and validation using `serializers.Serializer`.