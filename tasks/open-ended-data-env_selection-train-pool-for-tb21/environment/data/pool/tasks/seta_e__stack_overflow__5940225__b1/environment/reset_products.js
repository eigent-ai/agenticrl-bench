const { Sequelize, DataTypes } = require('sequelize');

const sequelize = new Sequelize({
  dialect: 'sqlite',
  storage: '/app/products.db',
  logging: false,
});

(async () => {
  await sequelize.query('DELETE FROM products');
  console.log('Products table cleared.');
  await sequelize.close();
})();
