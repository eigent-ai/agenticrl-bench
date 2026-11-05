import React from 'react';

function Toolbar({ categories, activeFilters, onFilterChange }) {
  const toggleFilter = (category) => {
    if (activeFilters.includes(category)) {
      onFilterChange(activeFilters.filter(f => f !== category));
    } else {
      onFilterChange([...activeFilters, category]);
    }
  };

  return (
    <div className="toolbar">
      <h3>Categories</h3>
      <div className="filter-list">
        {categories.map((cat) => (
          <label key={cat} className="filter-item">
            <input
              type="checkbox"
              checked={activeFilters.includes(cat)}
              onChange={() => toggleFilter(cat)}
            />
            {cat}
          </label>
        ))}
      </div>
    </div>
  );
}

export default Toolbar;
