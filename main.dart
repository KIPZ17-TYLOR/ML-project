// // import 'package:chatbt_eg/chat_pages/chat_page.dart';
// // import 'package:flutter/material.dart';

// // void main() {
// //   runApp(const MyApp());
// // }

// // class MyApp extends StatelessWidget {
// //   const MyApp({super.key});

// //   @override
// //   Widget build(BuildContext context) {
// //     return const MaterialApp(
// //         debugShowCheckedModeBanner: false, home: ChatScreen());
// //   }
// // }

import 'package:chatbt_eg/chat_pages/chat_history.dart';
import 'package:chatbt_eg/chat_pages/previous_chats_list.dart';
// import 'package:flutter/material.dart';
// // import 'package:chatbt_eg/chat_pages/chat_list_screen.dart';

// void main() {
//   runApp(const MyApp());
// }

// class MyApp extends StatelessWidget {
//   const MyApp({Key? key}) : super(key: key);

//   @override
//   Widget build(BuildContext context) {
//     return MaterialApp(
//       debugShowCheckedModeBanner: false,
//       title: 'ChatBT',
//       theme: ThemeData(
//         primarySwatch: Colors.deepPurple,
//       ),
//       home: ChatListScreen(), // Set ChatListScreen as the home screen
//     );
//   }
// }

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

void main() {
  runApp(
    ChangeNotifierProvider(
      create: (context) => ChatHistoryManager(),
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: ChatListScreen(),
    );
  }
}
