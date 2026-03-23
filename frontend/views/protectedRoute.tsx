import { useLogto } from '@logto/rn';
import { Button, Text, View } from 'react-native';

export const ProtectedRoute = () => {
  const { signIn, signOut, isAuthenticated } = useLogto();

  return (
    <div>
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
          //todo Replace the redirect URI with your own
          <Button title="Sign in" onPress={async () => signIn(process.env.LOGTO_REDIRECT_URL)} />
        </View>
      )}
    </div>
  );
};