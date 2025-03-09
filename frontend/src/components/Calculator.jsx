import React, { useState, useContext } from "react";
import axios from "axios";
import { UserContext } from "../context/UserContext";

const Calculator = () => {
  const { user } = useContext(UserContext);
  const [answers, setAnswers] = useState({});
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [manualInput, setManualInput] = useState("");
  const [result, setResult] = useState(null);
  const [detailedResults, setDetailedResults] = useState(null);

  const questions = [
    // IT Usage
    { id: "phone_calls", text: "How many phone calls do you make per month?", options: ["0", "1-50", "51-100", "101-200", "Enter manually"] },
    { id: "sms", text: "How many SMS do you send per month?", options: ["0", "1-50", "51-100", "101-200", "Enter manually"] },
    { id: "emails", text: "How many emails do you send per month?", options: ["0", "1-50", "51-100", "101-200", "Enter manually"] },
    { id: "spam_emails", text: "How many spam emails do you receive per month?", options: ["0", "1-100", "101-500", "501-1000", "Enter manually"] },
    { id: "emails_with_attachments", text: "How many emails with attachments do you send per month?", options: ["0", "1-50", "51-100", "101-200", "Enter manually"] },

    // Water Consumption
    { id: "water_usage", text: "How much water do you use per month (in cubic meters)?", options: ["0-5", "6-10", "11-15", "16-20", "Enter manually"] },

    // Business Travel
    { id: "flight_economy", text: "How far do you travel for business by economy class flights per month(in kilometers)?", options: ["0 km", "1-500 km", "501-1000 km", "1001-5000 km", "Enter manually"] },
    { id: "flight_first_class", text: "How far do you travel for business by first class flights per month(in kilometers)?", options: ["0 km", "1-500 km", "501-1000 km", "1001-5000 km", "Enter manually"] },
    { id: "taxi", text: "How far do you travel by taxi per month(in kilometers)?", options: ["0 km", "1-50 km", "51-100 km", "101-200 km", "Enter manually"] },

    // Transportation
    { id: "petrol_car", text: "How far do you drive a petrol car per month(in kilometers)?", options: ["0 km", "1-200 km", "201-500 km", "501-1000 km", "Enter manually"] },
    { id: "diesel_car", text: "How far do you drive a diesel car per month(in kilometers)?", options: ["0 km", "1-200 km", "201-500 km", "501-1000 km", "Enter manually"] },
    { id: "cng_car", text: "How far do you drive a CNG car per month(in kilometers)?", options: ["0 km", "1-200 km", "201-500 km", "501-1000 km", "Enter manually"] },
    { id: "motorbike", text: "How far do you travel by motorbike per month(in kilometers)?", options: ["0 km", "1-200 km", "201-500 km", "501-1000 km", "Enter manually"] },
    { id: "train", text: "How far do you travel by train per month(in kilometers)?", options: ["0 km", "1-200 km", "201-500 km", "501-1000 km", "Enter manually"] },
    { id: "bus", text: "How far do you travel by bus per month(in kilometers)?", options: ["0 km", "1-200 km", "201-500 km", "501-1000 km", "Enter manually"] },

    // Energy Consumption
    { id: "electricity", text: "How much electricity do you use per month(in KiloWatt per hour)?", options: ["0-100 kWh", "101-300 kWh", "301-600 kWh", "Enter manually"] },
    { id: "heating", text: "How much heating energy do you use per month(in KiloWatt per hour)?", options: ["0-100 kWh", "101-300 kWh", "301-600 kWh", "Enter manually"] },
    { id: "gas", text: "How much gas do you use per month(in cubic meters)?", options: ["0-5 m³", "6-10 m³", "11-20 m³", "Enter manually"] },

    // Waste Production
    { id: "paper_waste", text: "How much paper waste do you generate per month(in kilograms)?", options: ["0-5 kg", "6-10 kg", "11-20 kg", "Enter manually"] },
    { id: "plastic_waste", text: "How much plastic waste do you generate per month(in kilograms)?", options: ["0-5 kg", "6-10 kg", "11-20 kg", "Enter manually"] },
    { id: "glass_waste", text: "How much glass waste do you generate per month(in kilograms)?", options: ["0-5 kg", "6-10 kg", "11-20 kg", "Enter manually"] },
    { id: "general_waste", text: "How much general waste do you generate per month(in kilograms)?", options: ["0-5 kg", "6-20 kg", "21-50 kg", "Enter manually"] },
  ];

const handleAnswerChange = (questionId, value) => {
    setAnswers((prev) => ({
      ...prev,
      [questionId]: value === "Enter manually" ? manualInput : value
    }));
  };

  const handleManualInput = (e) => {
    setManualInput(e.target.value);
  };

  const handleSubmit = async () => {
    try {
      const formattedAnswers = Object.fromEntries(
        Object.entries(answers).map(([key, value]) => {
          if (value.includes("-")) {
            const [low, high] = value.split("-").map(Number);
            return [key, (low + high) / 2];  // Average value for ranges
          }
          return [key, isNaN(value) ? value : Number(value)];
        })
      );

      const response = await axios.post("http://127.0.0.1:8000/calculate", {
        answers: formattedAnswers
      });

      setResult(response.data.total_carbon_footprint_kg);
      setDetailedResults(response.data.category_breakdown);

    } catch (error) {
      console.error("Error calculating footprint:", error);
      alert("There was an error calculating the footprint. Please try again.");
    }
  };

  return (
    <div>
      <h1>Footprint Calculator</h1>
      {questions.map((question) => (
        <div key={question.id}>
          <h4>{question.text}</h4>
          <input
            type="text"
            placeholder="Enter a value"
            value={answers[question.id] || ""}
            onChange={(e) => handleAnswerChange(question.id, e.target.value)}
          />
        </div>
      ))}
      <button onClick={handleSubmit}>Calculate</button>

      {result !== null && (
        <div>
          <h3>Total Carbon Footprint: {result} kg CO₂/month</h3>
          <h4>Breakdown:</h4>
          <ul>
            {detailedResults &&
              Object.entries(detailedResults).map(([category, emission]) => (
                <li key={category}>
                  {category}: {emission.toFixed(2)} kg CO₂
                </li>
              ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Calculator;