import React, { useEffect, useState } from "react";
// 1. import `ChakraProvider` component
import { ChakraProvider } from '@chakra-ui/react'




const App = () => {
  const [message, setMessage] = useState("");
  const [posts, setPosts] = useState([]);

  const getWelcomeMessage = async () => {
    const requestOptions = {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    };

    const response = await fetch("http://localhost:8000/", requestOptions);
    const data = await response.json();

    if (!response.ok) {
      const error = (data && data.message) || response.status;
      return Promise.reject(error);
    } else {
      setMessage(data.message);
    }
  };

  useEffect(() => {
    getWelcomeMessage();
  }, []);

  const get_posts = async () => {
    const response = await fetch("http://localhost:8000/posts");
    const data = await response.json();

    console.log(data);

    if (!response.ok) {
      const error = (data && data.message) || response.status;
      return Promise.reject(error);
    } else {
      setPosts(data);
    }
  };

  useEffect(() => {
    get_posts();
  }, []);
  return (
    <div className="App">
      <h1>Stack: FastAPI , React , PostgreSQL</h1>
      <h1>{message}</h1>
      <h1>Posts</h1>
      {/* // map the posts and return it as a different array , this could be applied to any array. */}
      {posts.length>0 && posts.map((post) => (<BlogCard post={post} key={post.id}></BlogCard>))} 
    </div>
  );
};

// This is a react component: BlogCard
const BlogCard = ({ post }) => {
  return (
    <div>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </div>
          
  )
};

export default App;

// istekleri useeffect icinde kullan

