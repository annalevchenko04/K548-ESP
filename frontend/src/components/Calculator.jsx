import React, { useState, useContext } from "react";
import axios from "axios";
import { UserContext } from "../context/UserContext";
import { questions } from "../context/questions";  // Corrected Import Path

const Calculator = () => {
    const { user } = useContext(UserContext);
    const [answers, setAnswers] = useState({});
    const [result, setResult] = useState(null);
    const [detailedResults, setDetailedResults] = useState(null);

    const handleAnswerChange = (questionId, value) => {
        setAnswers((prev) => ({
            ...prev,
            [questionId]: value
        }));
    };

    const handleSubmit = async () => {
        try {
            const formattedAnswers = Object.fromEntries(
                Object.entries(answers).map(([key, value]) => {
                    if (value.includes("-")) {
                        const [low, high] = value.split("-").map(Number);
                        return [key, (low + high) / 2];
                    }
                    return [key, isNaN(value) ? value : Number(value)];
                })
            );

            const response = await axios.post("http://127.0.0.1:8000/footprint", {
                answers: formattedAnswers
            });

            const enrichedResults = Object.entries(response.data.category_breakdown).map(([category, emission]) => {
                const matchedQuestion = questions.find((q) => q.id === category);
                const displayText = matchedQuestion
                    ? `${matchedQuestion.text} (${matchedQuestion.unit})`
                    : category.replace(/_/g, " "); // Handle unmatched categories
                return {
                    id: category,
                    text: displayText,
                    emission: emission.toFixed(2)
                };
            });

            setResult(response.data.total_carbon_footprint_kg);
            setDetailedResults(enrichedResults);

        } catch (error) {
            alert("Error calculating footprint. Please try again.");
        }
    };

    const groupedQuestions = questions.reduce((acc, question) => {
        if (!acc[question.category]) {
            acc[question.category] = [];
        }
        acc[question.category].push(question);
        return acc;
    }, {});

    return (
        <div>
            <h1>Footprint Calculator</h1>

            {/* Render grouped questions with category headers */}
            {Object.entries(groupedQuestions).map(([category, categoryQuestions]) => (
                <div key={category} style={{ marginBottom: "20px" }}>
                    <h3 style={{ textTransform: "capitalize", fontWeight: "bold", marginBottom: "10px" }}>
                        {category.replace("_", " ")}
                    </h3>
                    {categoryQuestions.map((question) => (
                        <div key={question.id} style={{ marginBottom: "10px" }}>
                            <label htmlFor={question.id}>
                                {question.text} — <span style={{ fontWeight: "bold" }}>{question.id}</span> ({question.unit})
                            </label>
                            <input
                                type="text"
                                id={question.id}
                                placeholder={`Enter ${question.unit}`}
                                value={answers[question.id] || ""}
                                onChange={(e) => handleAnswerChange(question.id, e.target.value)}
                                style={{
                                    width: "100%",
                                    padding: "8px",
                                    marginTop: "4px",
                                    borderRadius: "5px",
                                    border: "1px solid #ccc"
                                }}
                            />
                        </div>
                    ))}
                </div>
            ))}

            <button
                onClick={handleSubmit}
                style={{
                    backgroundColor: "#4CAF50",
                    color: "white",
                    padding: "10px 20px",
                    border: "none",
                    borderRadius: "5px",
                    cursor: "pointer",
                    marginTop: "20px"
                }}
            >
                Calculate
            </button>

            {result !== null && (
                <div>
                    <h3>Total Carbon Footprint: {result} kg CO₂/month</h3>
                    <h4>Breakdown:</h4>
                    <ul>
                        {detailedResults &&
                            detailedResults.map(({ id, text, emission }) => (
                                <li key={id}>
                                    {text} — {emission} kg CO₂
                                </li>
                            ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default Calculator;
