import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Link, useNavigate } from 'react-router-dom';
import { toast } from 'react-hot-toast';
import api from '../../lib/axios';

export default function Register() {
  const { register, handleSubmit, watch, formState: { errors } } = useForm();
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const password = watch('password');

  const onSubmit = async (data: any) => {
    setIsLoading(true);
    try {
      await api.post('/auth/register/', {
        email: data.email,
        password: data.password,
        first_name: data.first_name,
        last_name: data.last_name
      });
      toast.success('Registration successful! Please login.');
      navigate('/login');
    } catch (error: any) {
      toast.error(error.response?.data?.email?.[0] || 'Registration failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center py-10">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <h2 className="text-2xl font-bold text-center mb-6 text-gray-800">Create an Account</h2>
        
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">First Name</label>
              <input 
                type="text" 
                {...register('first_name', { required: 'First name is required' })} 
                className={`mt-1 block w-full rounded-md border p-2 focus:ring-blue-500 focus:border-blue-500 ${errors.first_name ? 'border-red-500' : 'border-gray-300'}`}
              />
              {errors.first_name && <p className="mt-1 text-xs text-red-500">{errors.first_name.message as string}</p>}
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Last Name</label>
              <input 
                type="text" 
                {...register('last_name', { required: 'Last name is required' })} 
                className={`mt-1 block w-full rounded-md border p-2 focus:ring-blue-500 focus:border-blue-500 ${errors.last_name ? 'border-red-500' : 'border-gray-300'}`}
              />
              {errors.last_name && <p className="mt-1 text-xs text-red-500">{errors.last_name.message as string}</p>}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Email</label>
            <input 
              type="email" 
              {...register('email', { 
                required: 'Email is required',
                pattern: { value: /^\S+@\S+$/i, message: 'Invalid email address' }
              })} 
              className={`mt-1 block w-full rounded-md border p-2 focus:ring-blue-500 focus:border-blue-500 ${errors.email ? 'border-red-500' : 'border-gray-300'}`}
            />
            {errors.email && <p className="mt-1 text-xs text-red-500">{errors.email.message as string}</p>}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Password</label>
            <input 
              type="password" 
              {...register('password', { 
                required: 'Password is required',
                minLength: { value: 8, message: 'Password must be at least 8 characters' }
              })} 
              className={`mt-1 block w-full rounded-md border p-2 focus:ring-blue-500 focus:border-blue-500 ${errors.password ? 'border-red-500' : 'border-gray-300'}`}
            />
            {errors.password && <p className="mt-1 text-xs text-red-500">{errors.password.message as string}</p>}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Confirm Password</label>
            <input 
              type="password" 
              {...register('confirm_password', { 
                validate: value => value === password || 'Passwords do not match'
              })} 
              className={`mt-1 block w-full rounded-md border p-2 focus:ring-blue-500 focus:border-blue-500 ${errors.confirm_password ? 'border-red-500' : 'border-gray-300'}`}
            />
            {errors.confirm_password && <p className="mt-1 text-xs text-red-500">{errors.confirm_password.message as string}</p>}
          </div>

          <button 
            type="submit" 
            disabled={isLoading}
            className="w-full bg-blue-600 text-white p-2 rounded-md hover:bg-blue-700 transition duration-200 disabled:opacity-50 mt-4"
          >
            {isLoading ? 'Creating Account...' : 'Register'}
          </button>
        </form>

        <div className="mt-6 text-center text-sm">
          <p className="text-gray-600">
            Already have an account?{' '}
            <Link to="/login" className="text-blue-600 hover:underline">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
