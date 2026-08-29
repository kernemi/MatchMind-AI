import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { toast } from 'react-hot-toast';
import api from '../../lib/axios';
import { useAuth } from './AuthContext';

export default function Profile() {
  const { user, fetchUser } = useAuth();
  const { register, handleSubmit, formState: { errors }, reset } = useForm();
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (user) {
      reset({
        first_name: user.first_name,
        last_name: user.last_name,
        email: user.email,
      });
    }
  }, [user, reset]);

  const onSubmit = async (data: any) => {
    setIsLoading(true);
    try {
      await api.put('/auth/profile/', {
        first_name: data.first_name,
        last_name: data.last_name
      });
      toast.success('Profile updated successfully!');
      fetchUser();
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to update profile.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <div className="bg-white shadow rounded-lg overflow-hidden">
        <div className="px-4 py-5 sm:px-6 bg-gray-50">
          <h3 className="text-lg leading-6 font-medium text-gray-900">Profile Settings</h3>
          <p className="mt-1 max-w-2xl text-sm text-gray-500">Update your account information.</p>
        </div>
        
        <div className="px-4 py-5 sm:p-6">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <div className="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
              <div className="sm:col-span-3">
                <label className="block text-sm font-medium text-gray-700">First Name</label>
                <div className="mt-1">
                  <input
                    type="text"
                    {...register('first_name', { required: 'First name is required' })}
                    className={`block w-full rounded-md border p-2 focus:ring-blue-500 focus:border-blue-500 ${errors.first_name ? 'border-red-500' : 'border-gray-300'}`}
                  />
                  {errors.first_name && <p className="mt-1 text-xs text-red-500">{errors.first_name.message as string}</p>}
                </div>
              </div>

              <div className="sm:col-span-3">
                <label className="block text-sm font-medium text-gray-700">Last Name</label>
                <div className="mt-1">
                  <input
                    type="text"
                    {...register('last_name', { required: 'Last name is required' })}
                    className={`block w-full rounded-md border p-2 focus:ring-blue-500 focus:border-blue-500 ${errors.last_name ? 'border-red-500' : 'border-gray-300'}`}
                  />
                  {errors.last_name && <p className="mt-1 text-xs text-red-500">{errors.last_name.message as string}</p>}
                </div>
              </div>

              <div className="sm:col-span-6">
                <label className="block text-sm font-medium text-gray-700">Email Address (Read Only)</label>
                <div className="mt-1">
                  <input
                    type="email"
                    {...register('email')}
                    disabled
                    className="block w-full rounded-md border border-gray-300 p-2 bg-gray-100 text-gray-500 cursor-not-allowed"
                  />
                </div>
              </div>
            </div>

            <div className="flex justify-end">
              <button
                type="submit"
                disabled={isLoading}
                className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
              >
                {isLoading ? 'Saving...' : 'Save Changes'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
