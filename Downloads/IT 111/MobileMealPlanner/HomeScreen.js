import React, { useState } from "react";
import { View, Text, Button, TextInput } from "react-native";
import { Calendar } from "react-native-calendars";
import { collection, addDoc } from "firebase/firestore";
import { db } from "../firebaseConfig";

export default function HomeScreen() {
  const [selectedDate, setSelectedDate] = useState("");
  const [meal, setMeal] = useState("");

  const saveMealPlan = async () => {
    if (!selectedDate || !meal) {
      alert("Please select a date and enter a meal.");
      return;
    }
    await addDoc(collection(db, "mealPlans"), {
      date: selectedDate,
      meal,
    });
    alert("Meal plan saved!");
    setMeal("");
  };

  return (
    <View>
      <Calendar
        onDayPress={(day) => setSelectedDate(day.dateString)}
      />
      <Text>Selected Date: {selectedDate}</Text>
      <TextInput value={meal} onChangeText={setMeal} placeholder="Enter meal" />
      <Button title="Save Meal Plan" onPress={saveMealPlan} />
    </View>
  );
}
