# Dataset Dictionary & Documentation

*Note: This document contains only schema descriptions and metadata based on raw file inspection.*

## 1. Dataset 1: `aa_dataset-tickets-multi-lang-5-2-50-version.csv`
**Description:** A multilingual IT/Software support ticket dataset focusing on textual descriptions, categorization, and the final agent response.

### Column Dictionary
| Column | Data Type | Missing % | Unique | Likely Semantic Meaning |
|---|---|---|---|---|
| `subject` | String | 13.43% | 24,749 | The title/subject line of the ticket. |
| `body` | String | 0.00% | 28,587 | The full detailed description of the customer issue. |
| `answer` | String | 0.02% | 28,580 | The final resolution/response provided by the support agent. |
| `type` | String | 0.00% | 4 | Broad category of the ticket (e.g., Incident). |
| `queue` | String | 0.00% | 10 | The specific agent queue assigned (e.g., Technical Support). |
| `priority` | String | 0.00% | 3 | Urgency of the ticket (e.g., high). |
| `language` | String | 0.00% | 2 | Language of the ticket (e.g., 'de'). |
| `version` | Integer | 0.00% | 3 | Metadata / system versioning. |
| `tag_1` to `tag_8` | String | 0.0% to 98.0% | Varies | Multi-label descriptors (e.g., Security, Outage). High missingness on trailing tags. |

### Data Availability & Targets
- **Classification Targets:** `type`, `queue`, `priority`, `tag_*`.
- **RAG/GenAI:** `body` (Context) -> `answer` (Target).
- **Leakage Warning:** Do NOT use `answer` to predict `priority` or `type`, as `answer` is generated after triage.

---

## 2. Dataset 2: `customer_support_tickets.csv`
**Description:** A consumer-centric customer support dataset containing rich customer metadata, product info, and lifecycle timestamps.

### Column Dictionary
| Column | Data Type | Missing % | Unique | Likely Semantic Meaning |
|---|---|---|---|---|
| `Ticket ID` | Integer | 0.00% | 8,469 | Unique identifier. |
| `Customer Name` | String | 0.00% | 8,028 | PII - Customer name. |
| `Customer Email` | String | 0.00% | 8,320 | PII - Customer email. |
| `Customer Age` | Integer | 0.00% | 53 | Demographic info. |
| `Customer Gender` | String | 0.00% | 3 | Demographic info. |
| `Product Purchased` | String | 0.00% | 42 | Consumer product involved (e.g., GoPro Hero). |
| `Date of Purchase` | String | 0.00% | 730 | Date product was bought. |
| `Ticket Type` | String | 0.00% | 5 | Category (e.g., Technical issue). |
| `Ticket Subject` | String | 0.00% | 16 | Very low cardinality; likely a dropdown selection, not free text. |
| `Ticket Description` | String | 0.00% | 8,077 | The actual issue reported. |
| `Ticket Status` | String | 0.00% | 3 | Lifecycle state (e.g., Pending). |
| `Resolution` | String | 67.30% | 2,769 | The resolution text/action. Missing values imply open tickets. |
| `Ticket Priority` | String | 0.00% | 4 | Urgency label. |
| `Ticket Channel` | String | 0.00% | 4 | Source of ticket (e.g., Social media). |
| `First Response Time` | String(Date) | 33.29% | 5,470 | Timestamp of agent's first reply. |
| `Time to Resolution` | String(Date) | 67.30% | 2,728 | Timestamp of ticket closure. |
| `Customer Satisfaction Rating`| Float | 67.30% | 5 | CSAT score (1-5). |

### Data Availability & Targets
- **Classification Targets:** `Ticket Type`, `Ticket Priority`.
- **Regression Targets:** `Time to Resolution` (needs to be calculated dynamically from creation date).
- **Leakage Warning:** Do NOT use `Ticket Status`, `Resolution`, `First Response Time`, `Time to Resolution`, or `CSAT` to predict priority/type at creation time.

## 3. Dataset Suitability
- **Priority Prediction:** Fully supported by both datasets.
- **Categorization:** Fully supported by both datasets.
- **Resolution Time Prediction:** Partially supported by Dataset 2. Requires date parsing and handling of 67% missing values (open tickets).
- **Escalation Prediction:** NOT SUPPORTED. Neither dataset contains an explicit escalation flag. A proxy must be engineered later.
- **RAG Generation:** Fully supported by Dataset 1 (`body` to `answer`). Dataset 2's `Resolution` is too sparse (67% missing) and potentially low quality based on sample text.
