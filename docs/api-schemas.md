# API Schemas (Draft)

All responses include `id` and `timestamp` fields.

## Raw Data Endpoints

### Post
```json
{
  "id": "string",
  "timestamp": "ISO-8601",
  "subreddit": "string",
  "title": "string",
  "body": "string",
  "score": 0,
  "comment_count": 0
}
```

### Comment
```json
{
  "id": "string",
  "timestamp": "ISO-8601",
  "subreddit": "string",
  "post_id": "string",
  "body": "string",
  "score": 0
}
```

## Aggregated Analytics Endpoints

### Sentiment Series
```json
{
  "id": "string",
  "timestamp": "ISO-8601",
  "context": "global|subreddit|event",
  "label": "string",
  "sentiment": 0.0
}
```

### Trend Snapshot
```json
{
  "id": "string",
  "timestamp": "ISO-8601",
  "keyword": "string",
  "velocity": 0.0,
  "spike": 0.0,
  "context": "string"
}
```
