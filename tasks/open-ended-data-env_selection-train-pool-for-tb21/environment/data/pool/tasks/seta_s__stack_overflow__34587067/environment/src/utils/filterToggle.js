function toggleCategoryFilter(element, category) {
  var targetClass = 'hidden-' + category;
  if (!element.className.includes(targetClass)) {
    element.className = element.className + targetClass;
  } else {
    var pattern = new RegExp(category + '\\-hidden');
    element.className = element.className.replace(pattern, '').trim();
  }
}

module.exports = { toggleCategoryFilter };
