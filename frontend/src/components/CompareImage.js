import React, { useState, useRef } from "react";
import axios from "axios";
import CameraCapture from "./CameraCapture";

const CompareImage = () => {
  const [registrationNumber, setRegistrationNumber] = useState("");
  const [capturedImage, setCapturedImage] = useState(null);
  const [similarity, setSimilarity] = useState(null);
  const [verified, setVerified] = useState(null);
  const [message, setMessage] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [useCamera, setUseCamera] = useState(false);
  const [comparisonType, setComparisonType] = useState("deepface"); // افتراضي هو deepface

  const fileInputRef = useRef(null);

  const handleCompare = async (e) => {
    e.preventDefault();

    if (registrationNumber.length < 6) {
      setError("رقم التسجيل يجب أن يكون 6 أرقام على الأقل");
      return;
    }

    if (!capturedImage) {
      setError("يرجى اختيار صورة للمقارنة");
      return;
    }

    setError("");
    setLoading(true);
    setSimilarity(null);
    setVerified(null);
    setMessage(null);

    const formData = new FormData();
    formData.append("registration_number", registrationNumber);
    formData.append("captured_image", capturedImage);

    let apiUrl = "";
    if (comparisonType === "deepface") {
      apiUrl = "http://127.0.0.1:8000/api/compare_image_deepface"; // API لـ DeepFace
    } else if (comparisonType === "image_recognition") {
      apiUrl = "http://127.0.0.1:8000/api/compare_image_recognition"; // API لـ Image Recognition
    }

    try {
      const response = await axios.post(apiUrl, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      const similarityData =
        response.data.average_similarity || response.data.similarity;

      if (typeof similarityData === "object" && similarityData !== null) {
        setSimilarity(similarityData.threshold);
        setVerified(similarityData.verified);
      } else {
        setSimilarity(similarityData);
      }
      setMessage(response.data.message);
    } catch (error) {
      setError("فشلت عملية مقارنة الصور");
    } finally {
      setLoading(false);
      setRegistrationNumber("");
      setCapturedImage(null);

      if (fileInputRef.current) {
        fileInputRef.current.value = null;
      }
    }
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Compare Student Image</h2>
      <form onSubmit={handleCompare} className="space-y-4">
        <input
          type="text"
          placeholder="Registration Number"
          value={registrationNumber}
          onChange={(e) => setRegistrationNumber(e.target.value)}
          className="w-full p-2 border border-gray-300 rounded"
        />
        {error && <p className="text-red-500 text-sm">{error}</p>}

        <div className="flex gap-4">
          <button
            type="button"
            onClick={() => setUseCamera(false)}
            className={`w-1/2 p-2 rounded ${
              !useCamera ? "bg-blue-500 text-white" : "bg-gray-200"
            }`}
          >
            Choose Image
          </button>
          <button
            type="button"
            onClick={() => setUseCamera(true)}
            className={`w-1/2 p-2 rounded ${
              useCamera ? "bg-blue-500 text-white" : "bg-gray-200"
            }`}
          >
            Open Camera
          </button>
        </div>

        <div className="mt-4">
          <label className="mr-2">Choose Comparison Type:</label>
          <select
            value={comparisonType}
            onChange={(e) => setComparisonType(e.target.value)}
            className="p-2 border border-gray-300 rounded"
          >
            <option value="deepface">DeepFace</option>
            <option value="image_recognition">Image Recognition</option>
          </select>
        </div>

        {!useCamera && (
          <input
            type="file"
            ref={fileInputRef}
            onChange={(e) => setCapturedImage(e.target.files[0])}
            className="w-full p-2 border border-gray-300 rounded"
          />
        )}

        {useCamera && <CameraCapture setCapturedImage={setCapturedImage} />}

        <button
          type="submit"
          disabled={loading}
          className="w-full p-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          {loading ? "جاري المقارنة..." : "Compare Image"}
        </button>
      </form>

      {message && (
        <div className="mt-4 p-4 bg-green-100 border border-green-500 rounded">
          <h3 className="text-lg font-semibold">{message}</h3>
        </div>
      )}
      {similarity !== null && (
        <div className="mt-4 p-4 bg-blue-100 border border-blue-500 rounded">
          <h3 className="text-lg font-semibold">
            Similarity: {similarity.toFixed(2)}%
          </h3>
          <h3 className="text-lg font-semibold">
            Verified: {verified ? "Yes" : "No"}
          </h3>
        </div>
      )}
    </div>
  );
};

export default CompareImage;