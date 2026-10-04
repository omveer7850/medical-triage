const mongoose = require('mongoose');

const connectDB = async () => {
  try {
    const connStr = process.env.MONGO_URI || 'mongodb://localhost:27017/medical_triage';
    console.log(`Connecting to MongoDB at: ${connStr}`);
    
    // Connect to database
    await mongoose.connect(connStr, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    
    console.log('MongoDB connected successfully.');
  } catch (error) {
    console.error(`MongoDB connection error: ${error.message}`);
    // Do not crash the application in dev so it can run even without a running database
    console.log('Continuing without database connection...');
  }
};

module.exports = connectDB;
