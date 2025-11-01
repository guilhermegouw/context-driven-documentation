# Feature: {Feature Name}

> Living documentation for {feature-name} - maintained as the feature evolves

**Status:** [Production | Development | Deprecated]
**Version:** {version}
**Last Updated:** {date}

---

## Current Implementation Status

Brief overview of the feature's current state:
- Production status and deployment
- Major milestones and version history
- Current capabilities and limitations

---

## How It Works Today

### User Perspective
- What can users do with this feature?
- What are the main user flows?
- What value does it provide?

### System Behavior
- How does the system respond to user actions?
- What are the key workflows and processes?
- What constraints and limitations exist?

---

## Technical Implementation

### Architecture Overview
- High-level architecture and components
- Integration points with other systems
- Data flow and processing

### API Endpoints
```
GET /api/{resource}
POST /api/{resource}
PUT /api/{resource}/{id}
DELETE /api/{resource}/{id}
```

Brief description of each endpoint and its purpose.

### Data Models
```python
# Example data model structure
class FeatureModel:
    field1: str
    field2: int
    field3: Optional[datetime]
```

Key data models and their relationships.

### Key Files and Components
- `path/to/file.py:123` - Component description
- `path/to/another.py:456` - Another component
- `path/to/config.yaml` - Configuration

---

## Business Rules & Edge Cases

### Business Logic
- Core business rules and validations
- Calculation methods and formulas
- State transitions and workflows

### Edge Cases
- Known edge cases and how they're handled
- Boundary conditions and limits
- Error scenarios and recovery

### Validation Rules
- Input validation requirements
- Data integrity constraints
- Security and authorization rules

---

## Testing

### Test Coverage
- Unit test coverage and key test cases
- Integration test scenarios
- E2E test flows

### Known Issues
- Current bugs or limitations
- Workarounds in place
- Technical debt items

---

## Dependencies

### External Dependencies
- Third-party services or APIs
- Libraries and frameworks
- Infrastructure requirements

### Internal Dependencies
- Other features or modules
- Shared services or utilities
- Database or storage requirements

---

## Performance & Scalability

- Current performance characteristics
- Scalability considerations
- Optimization opportunities

---

## Security & Compliance

- Authentication and authorization
- Data privacy considerations
- Compliance requirements (if applicable)

---

## Future Enhancements

### Planned Improvements
- Upcoming features or changes
- Technical debt to address
- Performance optimizations

### Potential Expansions
- Ideas for future development
- User requests or feedback
- Architectural improvements

---

## Related Documentation

- Related features: `docs/features/related-feature.md`
- API documentation: `docs/api/endpoints.md`
- Architecture docs: `docs/architecture/system-design.md`

---

*This is a living document - update it as the feature evolves*
*Last reviewed: {date} by {reviewer}*
