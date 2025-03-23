import "./About.css";
import { FaReact, FaDocker, FaAws } from "react-icons/fa";
import { SiTailwindcss, SiHuggingface } from "react-icons/si";
import { SiFastapi } from "react-icons/si";
import aditya from './Github_Icons/aditya.jpg'; // Replace with your image
import { PiOpenAiLogo } from "react-icons/pi";
import { FaPython } from "react-icons/fa";
import { SiTerraform } from "react-icons/si";
import { CgVercel } from "react-icons/cg";
import { SiRender } from "react-icons/si";
import pinecone from '../assets/Pinecone.png';

const About = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      {/* Team Section */}
      <section id="Team" className="w-full py-8 bg-white shadow-md">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-8">Meet the Mastermind</h1>
        <div className="flex flex-col items-center">
          <div className="flex items-center justify-center space-x-6 mb-4">
            <div className="Person text-center">
              <img className="imageIcon rounded-full w-28 h-28 mx-auto" src={aditya} alt="Aditya Shah" />
              <div className="mt-3 text-base font-semibold">Aditya Shah</div>
              <div className="text-sm text-gray-600">Incoming Fry Cook at McDonald's</div>
              <div className="text-sm text-gray-600">(Also built this app between flipping burgers)</div>
            </div>
          </div>
        </div>
      </section>

      {/* Tech Stack Section */}
      <section id="TechStack" className="w-full py-8 bg-gray-50">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-8">My Tech Stack</h1>
        <div className="max-w-4xl mx-auto">
          <div className="overflow-hidden rounded-lg border border-gray-300">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-100">
                <tr>
                  <th className="py-3 px-6 text-left text-sm font-semibold text-gray-700">Section</th>
                  <th className="py-3 px-6 text-left text-sm font-semibold text-gray-700">Technology</th>
                  <th className="py-3 px-6 text-left text-sm font-semibold text-gray-700">Description</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                <tr>
                  <td className="py-3 px-6">AI Integration</td>
                  <td className="py-3 px-6 flex items-center space-x-4">
                    <SiHuggingface className="text-yellow-500 text-xl" />
                    <span>Hugging Face</span>
                    <PiOpenAiLogo className="text-green-500 text-xl" />
                    <span>OpenAI</span>
                    <img src={pinecone} alt="Pinecone" className="w-6 h-6" />
                    <span>Pinecone</span>
                  </td>
                  <td className="py-3 px-6">AI-driven resume builder because why not?</td>
                </tr>
                <tr>
                  <td className="py-3 px-6">Frontend</td>
                  <td className="py-3 px-6 flex items-center space-x-4">
                    <FaReact className="text-blue-500 text-xl" />
                    <span>React.js</span>
                    <SiTailwindcss className="text-blue-400 text-xl" />
                    <span>Tailwind CSS</span>
                  </td>
                  <td className="py-3 px-6">Fancy UI to distract you from my fry-cooking skills</td>
                </tr>
                <tr>
                  <td className="py-3 px-6">Backend</td>
                  <td className="py-3 px-6 flex items-center space-x-4">
                    <SiFastapi className="text-green-400 text-xl" />
                    <span>FastAPI</span>
                    <FaPython className="text-blue-500 text-xl" />
                    <span>Python</span>
                  </td>
                  <td className="py-3 px-6">RESTful APIs because REST is better than stress</td>
                </tr>
                <tr>
                  <td className="py-3 px-6">Deploy</td>
                  <td className="py-3 px-6 flex items-center space-x-4">
                    <FaAws className="text-orange-500 text-xl" />
                    <span>AWS</span>
                    <FaDocker className="text-blue-600 text-xl" />
                    <span>Docker</span>
                    <SiTerraform className="text-purple-600 text-xl" />
                    <span>Terraform</span>
                    <CgVercel className="text-black text-xl" />
                    <span>Vercel</span>
                    <SiRender className="text-indigo-500 text-xl" />
                    <span>Render</span>
                  </td>
                  <td className="py-3 px-6">Deployed so you can use it while I'm busy with fries</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </div>
  );
};

export default About;