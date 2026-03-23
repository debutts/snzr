import { useLogto } from '@logto/rn';
import { Button, Text, View } from 'react-native';

export const ProtectedRoute = () => {
  const { signIn, signOut, isAuthenticated } = useLogto();
  const LOGTO_REDIRECT_URL = process.env.EXPO_PUBLIC_LOGTO_REDIRECT_URL;
  const handleSignIn = async () => {
    await signIn(LOGTO_REDIRECT_URL);
  };

  return (
    <>
      {isAuthenticated ? (
        <View className="flex-1 items-center justify-center bg-white">
          <Text className="text-xl font-bold text-blue-500">
            Welcome to snzr, you are logged in!
          </Text>
          <Button title="Sign out" onPress={async () => signOut()} />
        </View>
      ) : (
        <View className="flex-1 items-center justify-center bg-white">
          <Text className="text-xl font-bold text-blue-500">
            Welcome to snzr!
          </Text>
          <Button title="Sign in" onPress={handleSignIn} />
        </View>
      )}
    </>
  );
};